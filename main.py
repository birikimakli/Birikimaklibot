import os
import requests
import feedparser

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"  # Linklerin ve kalın yazıların güzel görünmesi için
    }
    response = requests.post(url, data={k: v for k, v in payload.items() if v is not None})
    return response.text

def check_kap():
    # KAP Resmi RSS Akışı
    kap_rss_url = "https://www.kap.org.tr/tr/api/disseminor/rss/announcements/all"
    
    print("KAP RSS akışı okunuyor...")
    feed = feedparser.parse(kap_rss_url)
    
    # Eğer akış boşsa veya hata varsa
    if not feed.entries:
        print("KAP'tan veri alınamadı veya şu an yeni bildirim yok.")
        return

    # En son yayınlanan son 3 bildirimi alalım (Test amaçlı)
    latest_entries = feed.entries[:3]
    
    for entry in reversed(latest_entries): # Eskiden yeniye doğru sıralı göndermek için
        title = entry.title
        link = entry.link
        
        # Telegram için mesaj formatı oluşturma
        message = f"📢 *KAP BİLDİRİMİ*\n\n{title}\n\n🔗 [Detaylar için tıklayın]({link})"
        
        print(f"Gönderiliyor: {title}")
        send_telegram_message(message)

if __name__ == "__main__":
    check_kap()
