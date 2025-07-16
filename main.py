import discord
import os
import asyncio
import random
import sys
import datetime

# --- AYARLAR ---
try:
    TOKEN = os.environ['TOKEN']
    VOICE_CHANNEL_ID = int(os.environ['VOICE_CHANNEL_ID'])
except (KeyError, ValueError) as e:
    print(f"❌ HATA: Gerekli ortam değişkenleri bulunamadı veya hatalı: {e}")
    sys.exit(1)

STAY_ALIVE_INTERVAL = random.randint(25 * 60, 35 * 60) 
RECONNECT_DELAY = 15

client = discord.Client()
voice_client = None

# --- ANA FONKSİYONLAR ---

async def join_voice_channel():
    global voice_client
    try:
        channel = client.get_channel(VOICE_CHANNEL_ID)
        if isinstance(channel, discord.VoiceChannel):
            if voice_client and voice_client.is_connected():
                return
            
            print(f"🔗 \"{channel.name}\" kanalına bağlanma deneniyor...")
            voice_client = await channel.connect()
            print(f"🎧 Başarıyla \"{channel.name}\" kanalına bağlanıldı!")
        else:
            print(f"❌ HATA: {VOICE_CHANNEL_ID} ID'li bir ses kanalı bulunamadı.")
            await asyncio.sleep(60)
    except Exception as e:
        print(f"❌ Bağlanma hatası: {e}")
        await asyncio.sleep(RECONNECT_DELAY)
        await join_voice_channel()

async def stay_active():
    await asyncio.sleep(STAY_ALIVE_INTERVAL)
    
    while True:
        if voice_client and voice_client.is_connected():
            print("📢 AFK önleme: Kanaldan çıkıp tekrar giriliyor...")
            try:
                current_channel = voice_client.channel
                await voice_client.disconnect(force=True)
                voice_client = None
                print("📢 Başarıyla kanaldan ayrıldı.")
                await asyncio.sleep(random.randint(2, 5))
                await join_voice_channel()
            except Exception as e:
                print(f"📢 AFK önleme (çık-gir) hatası: {e}")
        else:
            print("📢 Aktif Kalma Kontrolü: Bağlantı kopuk. Yeniden bağlanma tetikleniyor.")
            await join_voice_channel()
        
        next_interval = random.randint(25 * 60, 35 * 60)
        print(f"📢 Bir sonraki AFK kontrolü {next_interval / 60:.1f} dakika sonra.")
        await asyncio.sleep(next_interval)
        
async def daily_restart():
    await asyncio.sleep(24 * 60 * 60)
    print("♻️ 24 saatlik çalışma süresi doldu. Stabilite için yeniden başlatılıyor...")
    sys.exit(0)

# --- OLAY (EVENT) YÖNETİCİLERİ ---

@client.event
async def on_ready():
    print(f'✅ {client.user.name} olarak giriş yapıldı!')
    await join_voice_channel()
    client.loop.create_task(stay_active())
    client.loop.create_task(daily_restart())

@client.event
async def on_voice_state_update(member, before, after):
    global voice_client
    if member.id == client.user.id and before.channel is not None and after.channel is None:
        print("⚠️ Ses kanalından düşüldü. Olay algılandı, yeniden bağlanılıyor...")
        voice_client = None
        await asyncio.sleep(RECONNECT_DELAY)
        await join_voice_channel()

# --- BAŞLATMA ---

try:
    # ******************************************************
    # *** DEĞİŞİKLİK BURADA: 'bot=False' PARAMETRESİ KALDIRILDI ***
    client.run(TOKEN)
    # ******************************************************
except Exception as e:
    print(f"❌ Giriş yapılamadı! Token geçersiz veya Discord'dan bir hata alındı: {e}")
