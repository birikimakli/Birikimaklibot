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
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    response = requests.post(url, data={k: v for k, v in payload.items() if v is not None})
    return response.text

def check_rss_feeds():
    # Sunucu engeline takılmayan, kesin veri dönen küresel ve yerel ekonomi akışları
    rss_urls = {
        "CNBC EKONOMİ (Global)": "https://search.cnbc.com/rs/search/all/view.rss?partnerId=2443&keywords=economy",
        "DÜNYA GAZETESİ (Ekonomi)": "https://www.dunya.com/rss",
        "BBC TÜRKÇE (Ekonomi)": "https://feeds.bbci.co.uk/turkce/rss.xml"
    }
    
    for source_name, url in rss_urls.items():
        print(f"🔄 {source_name} akışı okunuyor...")
        feed = feedparser.parse(url)
        
        if not feed.entries:
            print(f"⚠️ {source_name} şu an boş döndü, diğerine geçiliyor.")
            continue

        print(f"✅ {source_name} başarılı! Son haberler gönderiliyor...")
        
        # Test için her kararlı akıştan son 1 haberi çekelim
        latest_entry = feed.entries[0]
        title = latest_entry.title
        link = latest_entry.link
        
        message = f"📢 *{source_name}*\n\n{title}\n\n🔗 [Detaylar için tıklayın]({link})"
        
        print(f"🚀 Telegram'a gönderiliyor: {title}")
        send_telegram_message(message)
        break # En az bir tanesinden haber gönderdiysek testi başarıyla bitirelim

if __name__ == "__main__":
    check_rss_feeds()
