import discum
import os
from keep_alive import keep_alive

TOKEN = os.environ['TOKEN']
GUILD_ID = os.environ['GUILD_ID']
VOICE_CHANNEL_ID = os.environ['VOICE_CHANNEL_ID']

bot = discum.Client(token=TOKEN, log=True)

@bot.gateway.command
def on_ready(resp):
    if resp.event.ready_supplemental:
        print("[✓] Giriş yapıldı.")
        bot.gateway.removeCommand(on_ready)
        bot.sendVoiceState(GUILD_ID, VOICE_CHANNEL_ID)
        print("[✓] Ses kanalına bağlanma isteği gönderildi.")

keep_alive()
bot.gateway.run()
