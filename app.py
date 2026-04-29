"""
SecureWipe Pro v3.0 — Powered by VAJRA Algorithm
India's First Indigenous Data Sanitization Platform
Team TechnoGreen | BMIT Solapur | 2026
"""
import os, json, time, threading, uuid, logging
from flask import Flask, render_template, jsonify, request, send_file, Response, stream_with_context
from vajra_algorithm import vajra_wipe, VAJRAThreatScorer, HardwareDetector, VAJRA_VERSION
from cert_generator import generate_certificate, verify_certificate
from host_id_generator import get_host_id, generate_host_id, reset_host_id

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
app.secret_key = "securewipe_vajra_technogreen_2026"

BASE     = os.path.dirname(__file__)
CERT_DIR = os.path.join(BASE, "certs")
WIPE_DIR = os.path.join(BASE, "wipe_targets")
LOG_DIR  = os.path.join(BASE, "logs")
for d in [CERT_DIR, WIPE_DIR, LOG_DIR]:
    os.makedirs(d, exist_ok=True)

_sessions = {}
_stats    = {"total_wipes": 0, "total_certs": 0, "total_mb_wiped": 0}

VAJRA_STRATEGIES = {
    "vajra_lite":       {"passes":2,"label":"VAJRA-LITE","standard":"VAJRA v1.0","desc":"Quick — low risk personal data","color":"#00e5f0"},
    "vajra_std":        {"passes":3,"label":"VAJRA-STD","standard":"VAJRA v1.0 + NIST SP 800-88","desc":"Standard — personal & corporate","color":"#00ff88"},
    "vajra_high":       {"passes":5,"label":"VAJRA-HIGH","standard":"VAJRA v1.0 + DoD 5220.22-M","desc":"High — banking & healthcare","color":"#a855f7"},
    "vajra_max":        {"passes":7,"label":"VAJRA-MAX","standard":"VAJRA v1.0 + DoD 5220.22-M Ext","desc":"Maximum — sensitive enterprise","color":"#ff3b5c"},
    "vajra_brahmastra": {"passes":9,"label":"VAJRA-BRAHMASTRA","standard":"VAJRA v1.0 Supreme","desc":"Supreme — government & defence","color":"#ffc107"},
}

DATA_CATEGORIES = {
    "generic":"Generic / Unknown","personal":"Personal Data",
    "corporate":"Corporate / Business","healthcare":"Healthcare / Medical",
    "banking":"Banking / Finance","government":"Government / Aadhaar",
}

def get_drives():
    import psutil, platform
    drives = [{"device":"DEMO","mountpoint":"Demo Drive (Safe Simulation)","fstype":"DEMO",
               "total_gb":128.0,"used_gb":64.5,"free_gb":63.5,"percent":50,
               "drive_type":"Demo SSD 🔵","is_demo":True}]
    try:
        for p in psutil.disk_partitions(all=False):
            try:
                u = psutil.disk_usage(p.mountpoint)
                t = "NVMe SSD" if "nvme" in p.device.lower() else "SSD" if "sd" in p.device.lower() else "USB" if u.total<64e9 else "HDD"
                drives.append({"device":p.device,"mountpoint":p.mountpoint,"fstype":p.fstype,
                    "total_gb":round(u.total/1e9,1),"used_gb":round(u.used/1e9,1),
                    "free_gb":round(u.free/1e9,1),"percent":u.percent,"drive_type":t,"is_demo":False})
            except: pass
    except: pass
    return drives

def get_sysinfo():
    import psutil, platform
    try:
        cpu=psutil.cpu_percent(interval=0.1); mem=psutil.virtual_memory()
        return {"os":platform.system()+" "+platform.release(),"hostname":platform.node(),
                "cpu_percent":cpu,"ram_used_gb":round(mem.used/1e9,1),
                "ram_total_gb":round(mem.total/1e9,1),"ram_percent":mem.percent}
    except: return {"os":"Unknown","hostname":"Unknown","cpu_percent":0,"ram_percent":0,"ram_used_gb":0,"ram_total_gb":0}

@app.route("/")
def index(): return render_template("index.html")

@app.route("/api/drives")
def api_drives(): return jsonify(get_drives())

@app.route("/api/methods")
def api_methods(): return jsonify(VAJRA_STRATEGIES)

@app.route("/api/categories")
def api_categories(): return jsonify(DATA_CATEGORIES)

@app.route("/api/system")
def api_system(): return jsonify({**get_sysinfo(),**_stats})

@app.route("/api/host_id")
def api_host_id(): return jsonify(get_host_id())

@app.route("/api/host_id/reset", methods=["POST"])
def api_host_id_reset(): return jsonify({"status":"success","host_id":reset_host_id()})

@app.route("/api/threat_score", methods=["POST"])
def api_threat():
    d=request.json
    s=VAJRAThreatScorer()
    return jsonify(s.score(d.get("drive_type","SSD"),d.get("data_category","generic")))

@app.route("/api/wipe/start", methods=["POST"])
def api_start():
    d=request.json; drive=d.get("drive",{}); category=d.get("data_category","generic")
    size_mb=max(1,min(100,int(d.get("size_mb",5)))); sid=str(uuid.uuid4())
    _sessions[sid]={"progress":{"percent":0,"pass_label":"Initializing VAJRA...","pass":0,
        "total_passes":1,"pass_name":"","hex_preview":"","entropy":0,
        "written_mb":0,"total_mb":size_mb,"strategy":""},
        "done":False,"log":None,"cert":None,"error":None,
        "drive":drive,"category":category,"size_mb":size_mb,"events":[]}
    def run():
        target=os.path.join(WIPE_DIR,f"w_{sid[:8]}.bin")
        try:
            def cb(p):
                _sessions[sid]["progress"]=p
                _sessions[sid]["events"].append({"t":time.strftime("%H:%M:%S"),
                    "pass":p.get("pass",0),"label":p.get("pass_label",""),
                    "name":p.get("pass_name",""),"hex":p.get("hex_preview",""),
                    "entropy":p.get("entropy",0),"strategy":p.get("strategy","")})
            log=vajra_wipe(path=target,size_mb=size_mb,
                drive_label=drive.get("mountpoint","Unknown"),
                drive_type=drive.get("drive_type","SSD").replace(" 🔵",""),
                data_category=category,cb=cb)
            cert=generate_certificate(log,drive)
            _sessions[sid].update({"log":log,"cert":cert,"done":True})
            _stats["total_wipes"]+=1;_stats["total_certs"]+=1;_stats["total_mb_wiped"]+=size_mb
        except Exception as e:
            _sessions[sid].update({"error":str(e),"done":True})
        finally:
            if os.path.exists(target): os.remove(target)
    threading.Thread(target=run,daemon=True).start()
    return jsonify({"session_id":sid})

@app.route("/api/wipe/progress/<sid>")
def api_progress(sid):
    def gen():
        while True:
            s=_sessions.get(sid)
            if not s: yield f"data:{json.dumps({'error':'not found'})}\n\n"; break
            yield f"data:{json.dumps({**s['progress'],'done':s['done'],'error':s['error'],'events':s['events'][-5:]})}\n\n"
            if s["done"]: break
            time.sleep(0.15)
    return Response(stream_with_context(gen()),mimetype="text/event-stream",
                    headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no"})

@app.route("/api/wipe/result/<sid>")
def api_result(sid):
    s=_sessions.get(sid,{})
    if not s.get("done"): return jsonify({"error":"not ready"}),400
    c=s.get("cert",{})
    return jsonify({"cert_id":c.get("cert_id",""),"cert_data":c.get("cert_data",{}),"wipe_log":s.get("log",{})})

@app.route("/api/cert/pdf/<sid>")
def dl_pdf(sid):
    c=_sessions.get(sid,{}).get("cert",{})
    if not c: return "Not found",404
    return send_file(c["pdf_path"],as_attachment=True,download_name=f"VAJRA_WipeCert_{c['cert_id'][:8]}.pdf")

@app.route("/api/cert/json/<sid>")
def dl_json(sid):
    c=_sessions.get(sid,{}).get("cert",{})
    if not c: return "Not found",404
    return send_file(c["json_path"],as_attachment=True,download_name=f"VAJRA_WipeCert_{c['cert_id'][:8]}.json")

@app.route("/api/cert/qr/<sid>")
def get_qr(sid):
    c=_sessions.get(sid,{}).get("cert",{})
    if not c: return "Not found",404
    return send_file(c["qr_path"],mimetype="image/png")

@app.route("/api/verify",methods=["POST"])
def api_verify():
    f=request.files.get("cert_file")
    if not f: return jsonify({"valid":False,"error":"No file"})
    return jsonify(verify_certificate(f.read()))

if __name__=="__main__":
    print("\n"+"═"*60)
    print(f"  🔐  SecureWipe Pro v3.0")
    print(f"  ⚡  Powered by VAJRA Algorithm v{VAJRA_VERSION}")
    print(f"  🌐  Open: http://localhost:5000")
    print(f"  🏫  Team TechnoGreen | BMIT Solapur")
    print(f"  🇮🇳  India's First Indigenous Wipe Algorithm")
    print("═"*60+"\n")
    app.run(debug=True,port=5000,threaded=True)
