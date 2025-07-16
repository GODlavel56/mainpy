import discord
import os
from keep_alive import keep_alive
import asyncio

# Ortam değişkenlerini alıyoruz
TOKEN = os.environ['TOKEN']
# GUILD_ID bu kütüphanede doğrudan kullanılmıyor ama kontrol için kalabilir.
# GUILD_ID = os.environ['GUILD_ID'] 
VOICE_CHANNEL_ID = int(os.environ['VOICE_CHANNEL_ID']) # Kanal ID'sini integer yapmalıyız

# Client'ı oluşturuyoruz
client = discord.Client()

@client.event
async def on_ready():
    print(f'[✓] {client.user} olarak başarıyla giriş yapıldı.')
    print(f'[!] Ses kanalına bağlanılıyor: {VOICE_CHANNEL_ID}')
    
    try:
        # ID'sini verdiğimiz ses kanalını buluyoruz
        channel = client.get_channel(VOICE_CHANNEL_ID)
        
        if channel and isinstance(channel, discord.VoiceChannel):
            # Ses kanalına bağlanıyoruz
            await channel.connect()
            print(f'[✓] "{channel.name}" adlı ses kanalına başarıyla bağlanıldı.')
        else:
            print(f'[X] HATA: {VOICE_CHANNEL_ID} ID\'li bir ses kanalı bulunamadı veya bu bir ses kanalı değil.')
            
    except Exception as e:
        print(f'[X] HATA: Ses kanalına bağlanırken bir sorun oluştu: {e}')

# Sunucuyu canlı tutmak için keep_alive fonksiyonunu çalıştır
keep_alive()

try:
    # Botu çalıştırıyoruz.
    # bot=False parametresi, bunun bir kullanıcı tokeni olduğunu belirtir. BU ÇOK ÖNEMLİ!
    client.run(TOKEN, bot=False)
except discord.errors.LoginFailure:
    print("[X] HATA: Geçersiz bir token girildi. Lütfen Render'daki TOKEN değişkenini kontrol edin.")
except Exception as e:
    print(f"[X] HATA: Bot çalıştırılırken beklenmedik bir hata oluştu: {e}")
