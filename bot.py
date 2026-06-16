# ============================================
# DISCORD KEEP-ALIVE - REQUESTS ONLY
# No discord.py needed at all!
# ============================================

import requests
import os
import time
from datetime import datetime
import threading
from flask import Flask, jsonify
import json

# ============================================
# CONFIGURATION
# ============================================

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("❌ DISCORD_TOKEN environment variable not set!")

STATUS = os.environ.get("DISCORD_STATUS", "🎮 Online")

# ============================================
# FLASK WEB SERVER
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    return 'pong'

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ============================================
# DISCORD FUNCTIONS
# ============================================

def get_user_info():
    """Get user info to verify token works"""
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(
            "https://discord.com/api/v9/users/@me",
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Logged in as: {data.get('username')}#{data.get('discriminator')}")
            print(f"🆔 User ID: {data.get('id')}")
            return data
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def set_status():
    """Set Discord status using API directly"""
    headers = {
        "Authorization": TOKEN,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    payload = {
        "status": "online",
        "activities": [
            {
                "name": STATUS,
                "type": 0  # 0 = Playing
            }
        ],
        "afk": False
    }
    
    try:
        response = requests.patch(
            "https://discord.com/api/v9/users/@me/settings",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            print(f"✅ Status updated to: {STATUS}")
            return True
        else:
            print(f"❌ Failed to update status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error setting status: {e}")
        return False

def keep_alive_loop():
    """Keep the account alive"""
    print("🔄 Keep-alive loop started")
    
    # Get user info first
    user = get_user_info()
    if not user:
        print("❌ Token invalid! Please check your Discord token.")
        return
    
    # Set initial status
    set_status()
    
    # Update every 4 minutes
    while True:
        time.sleep(240)  # 4 minutes
        set_status()
        print(f"💓 Keep-alive at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started on port 8080")
    print("=" * 50)
    print("🚀 Discord Keep-Alive Starting...")
    print("=" * 50)
    
    # Start keep-alive in background
    keep_alive_thread = threading.Thread(target=keep_alive_loop, daemon=True)
    keep_alive_thread.start()
    
    # Keep main thread alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
