import discord
from discord.ext import commands
import os
from datetime import datetime
import threading
from flask import Flask, jsonify

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    raise Exception("❌ DISCORD_TOKEN environment variable not set!")

STATUS = os.environ.get("DISCORD_STATUS", "🎮 Online")

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

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Use commands.Bot for bot accounts
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("=" * 50)
    print("✅ DISCORD BOT IS ONLINE!")
    print("=" * 50)
    print(f"📡 Logged in as: {bot.user.name}")
    print(f"🆔 User ID: {bot.user.id}")
    print(f"💬 Status: {STATUS}")
    print("=" * 50)
    
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=STATUS)
    )

@bot.event
async def on_message(message):
    await bot.process_commands(message)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started")
    print("🚀 Starting Discord bot...")
    
    try:
        bot.run(TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid token! Please check your Discord token.")
    except Exception as e:
        print(f"❌ Error: {e}")
