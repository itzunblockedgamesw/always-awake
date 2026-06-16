# ============================================
# DISCORD USER ACCOUNT KEEP-ALIVE
# Using discord.py-self for user tokens
# ============================================

import discord
from discord.ext import commands
import os
from datetime import datetime
import threading
from flask import Flask, jsonify
import asyncio

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
        'user': bot.user.name if bot.user else 'unknown',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/ping')
def ping():
    return 'pong'

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# ============================================
# DISCORD CLIENT - Using discord.py-self
# ============================================

# Use self_bot=True for user accounts
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
intents.guilds = True

# This is the key - use self_bot=True
bot = commands.Bot(
    command_prefix='!', 
    self_bot=True,  # IMPORTANT: This enables user account mode
    intents=intents
)

@bot.event
async def on_ready():
    print("=" * 50)
    print("✅ DISCORD USER ACCOUNT IS ONLINE!")
    print("=" * 50)
    print(f"📡 Logged in as: {bot.user.name}")
    print(f"🆔 User ID: {bot.user.id}")
    print(f"💬 Status: {STATUS}")
    print(f"📅 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    # Set status
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=STATUS)
    )

@bot.event
async def on_message(message):
    await bot.process_commands(message)

# Simple commands
@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

@bot.command(name='status')
async def set_status(ctx, *, status):
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name=status)
    )
    await ctx.send(f"✅ Status changed to: {status}")

# ============================================
# STARTUP
# ============================================

if __name__ == "__main__":
    # Start Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Web server started")
    print("🚀 Starting Discord client with discord.py-self...")
    print("=" * 50)
    
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"❌ Error: {e}")
