import discord
import os
from keep_alive import keep_alive
import asyncio

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

keep_alive()

try:
    client.run(TOKEN, bot=False)
except discord.errors.LoginFailure:
    print("[X] HATA: Geçersiz bir token girildi. Lütfen Render'daki TOKEN değişkenini kontrol edin.")
except Exception as e:
    print(f"[X] HATA: Bot çalıştırılırken beklenmedik bir hata oluştu: {e}")