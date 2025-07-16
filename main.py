import discum
import os
from keep_alive import keep_alive
import time

TOKEN = os.environ['TOKEN']
GUILD_ID = os.environ['GUILD_ID']
VOICE_CHANNEL_ID = os.environ['VOICE_CHANNEL_ID']

# discum Client ayarları
bot = discum.Client(
    token=TOKEN,
    log=True,
    build_num=280800,
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
)

# Ses kanalına katılmak için yeni bir fonksiyon deniyoruz
def join_voice_channel():
    print("\n[!] Ses kanalına katılma fonksiyonu çalıştırıldı.")
    try:
        # Kütüphanenin kendi joinVoiceChannel fonksiyonunu kullanıyoruz
        bot.gateway.joinVoiceChannel(GUILD_ID, VOICE_CHANNEL_ID, self_deaf=True)
        print("[✓] Ses kanalına katılma isteği BAŞARIYLA gönderildi.")
    except Exception as e:
        print(f"[X] HATA: Ses kanalına katılma sırasında bir sorun oluştu: {e}")

@bot.gateway.command
def on_ready(resp):
    if resp.event.ready:
        print("\n[✓] Gateway'de 'READY' olayı başarıyla alındı. Hesap online.")
        bot.gateway.removeCommand(on_ready)
        
        # Fonksiyonu çağırmadan önce kısa bir bekleme süresi ekleyelim
        time.sleep(3)
        
        join_voice_channel()

print("[!] Script başlatıldı, keep_alive ayarlanıyor...")
keep_alive()
print("[!] Gateway çalıştırılıyor ve Discord'a bağlanılıyor...")
bot.gateway.run()
