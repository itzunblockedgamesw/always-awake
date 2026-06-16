# ============================================
# DISCORD USER ACCOUNT KEEP-ALIVE
# FOR USER TOKENS (from browser)
# ============================================

import discord
import os
from datetime import datetime
import threading
from flask import Flask, jsonify

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
# DISCORD CLIENT - USE Client() NOT Bot()!
# ============================================

# Use discord.Client() for user tokens
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("=" * 50)
    print("✅ DISCORD USER ACCOUNT IS ONLINE!")
    print("=" * 50)
    print(f"📡 Logged in as: {client.user.name}")
    print(f"🆔 User ID: {client.user.id}")
    print(f"💬 Status: {STATUS}")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Set status once - never changes
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=STATUS)
    )

@client.event
async def on_message(message):
    # Do nothing - just stay online
    pass

@client.event
async def on_error(event, *args, **kwargs):
    print(f"⚠️ Error in {event}")

# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    # Start Flask web server
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started on port 8080")
    print("🚀 Starting Discord client...")
    print("=" * 50)
    
    try:
        # Run with user token
        client.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Please check your Discord token.")
        print("💡 Make sure you're using a USER token (from browser) not a BOT token")
    except Exception as e:
        print(f"❌ Error: {e}")
