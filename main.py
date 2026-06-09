import os
import requests
import feedparser
import subprocess

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CACHE_FILE = "gonderilenler.txt"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data={k: v for k, v in payload.items() if v is not None})
    return response.text

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f.readlines())
    return set()

def save_to_cache(link):
    with open(CACHE_FILE, "a", encoding="utf-8") as f:
        f.write(link + "\n")

def push_changes_to_github():
    # GitHub Actions'ın hafıza dosyasını depoya geri kaydetmesi için Git ayarları
    try:
        subprocess.run(["git", "config", "--global", "user.name", "BirikimAkliBot"], check=True)
        subprocess.run(["git", "config", "--global", "user.email", "bot@birikimakli.local"], check=True)
        subprocess.run(["git", "add", CACHE_FILE], check=True)
        
        # Değişiklik var mı kontrol et
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", "🤖 Hafıza güncellendi [skip ci]"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("💾 Yeni haberler hafızaya kaydedildi ve GitHub'a yüklendi.")
        else:
            print("💤 Yeni bir haber olmadığı için hafıza güncellenmedi.")
    except Exception as e:
        print(f"⚠️ Git push hatası: {e}")

def check_rss_feeds():
    rss_urls = {
        "DÜNYA GAZETESİ (Ekonomi)": "https://www.dunya.com/rss",
        "CNBC EKONOMİ (Global)": "https://search.cnbc.com/rs/search/all/view.rss?partnerId=2443&keywords=economy"
    }
    
    cache = load_cache()
    new_news_sent = False
    
    for source_name, url in rss_urls.items():
        print(f"🔄 {source_name} akışı okunuyor...")
        feed = feedparser.parse(url)
        
        if not feed.entries:
            continue

        # En güncel son 3 haberi kontrol edelim
        latest_entries = feed.entries[:3]
        
        for entry in reversed(latest_entries):
            title = entry.title
            link = entry.link
            
            # EĞER HABER DAHA ÖNCE GÖNDERİLMEDİYSE
            if link not in cache:
                message = f"📢 *{source_name}*\n\n{title}\n\n🔗 [Detaylar için tıklayın]({link})"
                print(f"🚀 Yeni haber Telegram'a gönderiliyor: {title}")
                
                send_telegram_message(message)
                save_to_cache(link)
                cache.add(link) # Aynı döngüde tekrar takılmasın
                new_news_sent = True
                
        if new_news_sent:
            break # Bir kaynaktan yeni haber gönderdiysek bu turluk yeterli
            
    if new_news_sent:
        push_changes_to_github()

if __name__ == "__main__":
    check_rss_feeds()
