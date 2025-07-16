import discum
import os
from flask import Flask
from threading import Thread
import time

# --- Keep Alive Sunucu Kodu ---
# Bu kısım, Replit gibi platformlarda projenin sürekli çalışmasını sağlar.
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
GUILD_ID = os.environ['GUILD_ID']      # ID'leri string olarak almak daha güvenlidir.
VOICE_CHANNEL_ID = os.environ['VOICE_CHANNEL_ID']

# Bot istemcisini loglamayı açarak ve daha güncel bir build_num ile başlatıyoruz.
bot = discum.Client(
    token=TOKEN,
    log=True
)

# Ses kanalına katılma işlemini discum'a bırakıyoruz.
# Bu fonksiyon, kalp atışları dahil tüm ses bağlantı yönetimini otomatik yapar.
def join_voice_channel():
    print("[!] Ses kanalına katılınıyor...")
    # Not: discum eski bir kütüphane olduğu için bazen doğrudan fonksiyonlar
    # bekendiği gibi çalışmayabilir. Bu yüzden olayları dinleyerek manuel bir
    # akış oluşturuyoruz fakat bu sefer discum'un kendi araçlarıyla.
    
    # Botu başlat ve hazır olmasını bekle
    bot.gateway.run(auto_reconnect=True)


@bot.gateway.command
def on_ready(resp):
    if resp.event.ready:
        print("[✓] Gateway'e bağlanıldı ve READY olayı alındı.")
        
        # discum'un kendi fonksiyonunu kullanarak ses kanalına giriş yap
        # mute ve deaf parametrelerini burada belirtiyoruz.
        bot.joinVoiceChannel(GUILD_ID, VOICE_CHANNEL_ID, self_mute=True, self_deaf=True)
        print(f"[✓] Ses kanalına ({VOICE_CHANNEL_ID}) katılma isteği discum üzerinden gönderildi.")

# Projeyi başlat
keep_alive() # Flask sunucusunu başlat
print("[!] discum botu başlatılıyor...")

# Botu çalıştır. on_ready içerisindeki komut bot hazır olunca çalışacaktır.
bot.gateway.run(auto_reconnect=True)
