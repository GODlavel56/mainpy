import discord
import asyncio
import os
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']
VOICE_CHANNEL_ID = int(os.environ['VOICE_CHANNEL_ID'])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[✓] Giriş yapıldı: {client.user}")
    channel = client.get_channel(VOICE_CHANNEL_ID)
    if channel and isinstance(channel, discord.VoiceChannel):
        await channel.connect()
        print("[✓] Ses kanalına bağlanıldı.")
    else:
        print("[!] Ses kanalı bulunamadı veya geçersiz.")

keep_alive()
client.run(TOKEN, bot=False)
