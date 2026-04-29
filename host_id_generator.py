"""LocalHost ID Generator — Persistent Machine Identifier"""
import os, json, uuid, hashlib, platform
from datetime import datetime, timezone

HOST_ID_FILE = os.path.join(os.path.dirname(__file__), "certs", "host_id.json")

def get_machine_fingerprint():
    """Generate fingerprint from hardware/OS info"""
    try:
        import psutil
        cpu_info = f"{platform.processor()}_{psutil.cpu_count()}"
    except:
        cpu_info = platform.processor()
    
    os_info = f"{platform.system()}_{platform.release()}_{platform.node()}"
    combined = f"{os_info}_{cpu_info}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16].upper()

def generate_host_id():
    """Generate and persist a unique localhost ID"""
    os.makedirs(os.path.dirname(HOST_ID_FILE), exist_ok=True)
    
    # Check if host ID already exists
    if os.path.exists(HOST_ID_FILE):
        try:
            with open(HOST_ID_FILE, 'r') as f:
                data = json.load(f)
                return data
        except:
            pass
    
    # Generate new host ID
    host_id = {
        "host_id": str(uuid.uuid4()).upper(),
        "machine_fingerprint": get_machine_fingerprint(),
        "hostname": platform.node(),
        "os": f"{platform.system()} {platform.release()}",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "version": "1.0"
    }
    
    # Persist to file
    with open(HOST_ID_FILE, 'w') as f:
        json.dump(host_id, f, indent=2)
    
    return host_id

def get_host_id():
    """Retrieve the persistent localhost ID"""
    if os.path.exists(HOST_ID_FILE):
        try:
            with open(HOST_ID_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return generate_host_id()

def reset_host_id():
    """Reset and regenerate the host ID"""
    if os.path.exists(HOST_ID_FILE):
        os.remove(HOST_ID_FILE)
    return generate_host_id()

if __name__ == "__main__":
    host_info = generate_host_id()
    print(json.dumps(host_info, indent=2))
