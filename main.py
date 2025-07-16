import discord
import os
import asyncio
from flask import Flask
from threading import Thread

# --- Keep Alive Sunucu Kodu ---
app = Flask('')

@app.route('/')
def home():
    return "Bot çalışıyor."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# --- Sunucu Kodu Bitişi ---


# --- Discord Bot Kodu ---
TOKEN = os.environ['TOKEN']
VOICE_CHANNEL_ID = int(os.environ['VOICE_CHANNEL_ID'])

client = discord.Client()

@client.event
async def on_ready():
    print(f'[✓] {client.user} olarak başarıyla giriş yapıldı.')
    print(f'[!] Ses kanalına bağlanılıyor: {VOICE_CHANNEL_ID}')
    
    try:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            await channel.connect()
            print(f'[✓] "{channel.name}" adlı ses kanalına başarıyla bağlanıldı.')
        else:
            print(f'[X] HATA: {VOICE_CHANNEL_ID} ID\'li bir ses kanalı bulunamadı veya bu bir ses kanalı değil.')
            
    except Exception as e:
        print(f'[X] HATA: Ses kanalına bağlanırken bir sorun oluştu: {e}')

# Sunucuyu ve botu başlat
keep_alive()

try:
    # Son düzeltme burada: bot=False parametresi kaldırıldı.
    client.run(TOKEN)
except discord.errors.LoginFailure:
    print("[X] HATA: Geçersiz bir token girildi. Lütfen Render'daki TOKEN değişkenini kontrol edin.")
except Exception as e:
    print(f"[X] HATA: Bot çalıştırılırken beklenmedik bir hata oluştu: {e}")
