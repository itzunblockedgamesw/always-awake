# ============================================
# DISCORD ACCOUNT KEEP-ALIVE - DEBUG VERSION
# ============================================

import discord
import os
from datetime import datetime
import threading
from flask import Flask, jsonify
import sys

# ============================================
# CONFIGURATION
# ============================================

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("❌ DISCORD_TOKEN environment variable not set!")

STATUS = os.environ.get("DISCORD_STATUS", "🎮 Online")

# Debug: Show token format (first few chars only for security)
print(f"🔍 Token starts with: {TOKEN[:20]}...")
print(f"🔍 Token length: {len(TOKEN)}")
print(f"🔍 Token parts: {len(TOKEN.split('.'))} parts" if '.' in TOKEN else "No dots found")

# ============================================
# FLASK WEB SERVER
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'user': bot.user.name if bot.user else 'unknown',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    return 'pong'

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'token_loaded': bool(TOKEN),
        'token_length': len(TOKEN) if TOKEN else 0,
        'bot_running': bot.is_ready() if hasattr(bot, 'is_ready') else False
    })

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ============================================
# DISCORD CLIENT WITH BETTER ERROR HANDLING
# ============================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("=" * 50)
    print("✅ DISCORD BOT IS ONLINE!")
    print("=" * 50)
    print(f"📡 Logged in as: {bot.user.name}")
    print(f"🆔 User ID: {bot.user.id}")
    print(f"💬 Status: {STATUS}")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=STATUS)
    )

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"❌ Error in {event}: {sys.exc_info()}")

@bot.event
async def on_message(message):
    pass

# ============================================
# STARTUP WITH BETTER ERROR HANDLING
# ============================================

if __name__ == "__main__":
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started")
    print("🚀 Starting Discord bot...")
    print("=" * 50)
    
    try:
        # Try to run the bot with detailed error handling
        bot.run(TOKEN)
    except discord.LoginFailure as e:
        print(f"❌ Login failure: {e}")
        print("\n🔍 DEBUG INFO:")
        print(f"Token format: {TOKEN[:10]}...{TOKEN[-10:]}")
        print(f"Token parts: {len(TOKEN.split('.')) if '.' in TOKEN else 'No dots'}")
        print("\n💡 Possible issues:")
        print("1. You're using a Bot Token but trying to login as a User")
        print("2. The token is expired or revoked")
        print("3. The token is malformed (missing parts)")
        print("\n🔧 FIXES:")
        print("• For Bot Account: Use commands.Bot instead of discord.Client")
        print("• For User Account: Get token from browser's authorization header")
        print("• Regenerate the token if it's a bot token")
    except discord.HTTPException as e:
        print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
