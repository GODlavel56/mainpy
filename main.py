import discum
import os
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']
GUILD_ID = os.environ['GUILD_ID']
VOICE_CHANNEL_ID = os.environ['VOICE_CHANNEL_ID']

# Discord'un güncel sürüm bilgilerini manuel olarak ekliyoruz
bot = discum.Client(
    token=TOKEN,
    log=True,
    # discum'un otomatik bulmaya çalıştığı sürüm numarasını elle giriyoruz.
    # Bu numara zamanla eskiyebilir, hata alırsanız artırmayı deneyin.
    build_num=280800, 
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
)

@bot.gateway.command
def on_ready(resp):
    # 'ready_supplemental' yerine daha genel olan 'ready' olayını dinliyoruz
    if resp.event.ready:
        print("[✓] Giriş yapıldı ve READY olayı alındı.")
        bot.gateway.removeCommand(on_ready)
        bot.sendVoiceState(GUILD_ID, VOICE_CHANNEL_ID, self_deaf=True) # Kendini sağırlaştırma eklendi
        print(f"[✓] {GUILD_ID} sunucusundaki {VOICE_CHANNEL_ID} ses kanalına bağlanma isteği gönderildi.")

keep_alive()
bot.gateway.run()
