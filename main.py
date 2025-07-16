import discum
import os
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


# --- discum Bot Kodu ---
TOKEN = os.environ['TOKEN']
GUILD_ID = int(os.environ['GUILD_ID'])
VOICE_CHANNEL_ID = int(os.environ['VOICE_CHANNEL_ID'])


bot = discum.Client(
    token=TOKEN,
    log=True,
    build_num=280800,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
)

@bot.gateway.command
def on_ready(resp):
    if resp.event.ready:
        print("[✓] Gateway'e bağlanıldı ve READY olayı alındı.")
        bot.gateway.removeCommand(on_ready)
        
        # --- YENİ VE KESİN YÖNTEM: Komutu manuel olarak hazırlıyoruz ---
        # Bu, Discord'un ses durumu güncelleme komutudur (Opcode 4).
        payload = {
            "op": 4,
            "d": {
                "guild_id": GUILD_ID,
                "channel_id": VOICE_CHANNEL_ID,
                "self_mute": True,
                "self_deaf": True,
            }
        }
        
        # Hazırladığımız komutu doğrudan gateway'e gönderiyoruz.
        bot.gateway.send(payload)
        print(f"[✓] Ses kanalına ({VOICE_CHANNEL_ID}) katılma isteği doğrudan gönderildi.")

# Projeyi başlat
keep_alive()
print("[!] discum botu başlatılıyor...")
bot.gateway.run(auto_reconnect=True)
