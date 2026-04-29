"""
🔗 Generate Live Link for SecureWipe Pro
For Hackathon Demo
"""
import subprocess
import time
from pyngrok import ngrok

def generate_live_link():
    """Generate a live public URL for your SecureWipe Pro app"""
    
    # Auth token is already configured globally
    
    print("\n" + "="*70)
    print("  🔐 SecureWipe Pro - Live Link Generator")
    print("  🌐 Creating public tunnel...")
    print("="*70 + "\n")
    
    try:
        # Create tunnel to localhost:5000
        public_url = ngrok.connect(5000, "http")
        
        print(f"✅ SUCCESS! Your live link is ready:\n")
        print(f"🔗 Public URL: {public_url}")
        print(f"\n📋 Share this link for hackathon demo:")
        print(f"   {public_url}\n")
        
        print("="*70)
        print("  Keep this window open to keep the link active")
        print("  Press CTRL+C to stop")
        print("="*70 + "\n")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n⚠️  Make sure:")
        print(f"   1. Your app is running on http://localhost:5000")
        print(f"   2. ngrok token is set correctly")
        print(f"   3. You have internet connection")

if __name__ == "__main__":
    generate_live_link()
