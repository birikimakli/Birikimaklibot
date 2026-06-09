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
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data={k: v for k, v in payload.items() if v is not None})
    return response.text

def check_rss_feeds():
    # KAP'ın yanına alternatifi de ekledik ki Telegram'ı test edebilelim
    rss_urls = {
        "KAP BİLDİRİMİ": "https://www.kap.org.tr/tr/api/disseminor/rss/announcements/all",
        "EKONOMİ HABERİ": "https://bigpara.hurriyet.com.tr/rss/"
    }
    
    for source_name, url in rss_urls.items():
        print(f"🔄 {source_name} akışı okunuyor: {url}")
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"⚠️ {source_name} akışından veri alınamadı veya şu an boş.")
            continue

        # Son 2 haberi çekelim
        latest_entries = feed.entries[:2]
        
        for entry in reversed(latest_entries):
            title = entry.title
            link = entry.link
            
            message = f"📢 *{source_name}*\n\n{title}\n\n🔗 [Detaylar için tıklayın]({link})"
            
            print(f"🚀 Telegram'a gönderiliyor: {title}")
            send_telegram_message(message)

if __name__ == "__main__":
    check_rss_feeds()
