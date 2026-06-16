# ============================================
# DISCORD ACCOUNT KEEP-ALIVE
# For Render.com - SECURE VERSION
# ============================================

import discord
import os
from datetime import datetime
import threading
from flask import Flask, jsonify

# ============================================
# CONFIGURATION - READ FROM ENVIRONMENT
# ============================================

# Get token from environment variable (NEVER hardcode!)
TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("❌ DISCORD_TOKEN environment variable not set!")

# Get status from environment or use default
STATUS = os.environ.get("DISCORD_STATUS", "🎮 Online")

# ============================================
# FLASK WEB SERVER
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'user': client.user.name if client.user else 'unknown',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    return 'pong'

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ============================================
# DISCORD CLIENT
# ============================================

client = discord.Client()

@client.event
async def on_ready():
    print("=" * 50)
    print("✅ DISCORD ACCOUNT IS ONLINE!")
    print("=" * 50)
    print(f"📡 Logged in as: {client.user.name}")
    print(f"🆔 User ID: {client.user.id}")
    print(f"💬 Status: {STATUS}")
    print("=" * 50)
    
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=STATUS)
    )

@client.event
async def on_message(message):
    pass  # Just stay online

# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started")
    
    try:
        client.run(TOKEN)
    except Exception as e:
        print(f"❌ Error: {e}")
