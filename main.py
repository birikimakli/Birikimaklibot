import urllib.request
import xml.etree.ElementTree as ET

# === TELEGRAM BİLGİLERİNİZİ BURAYA YAZIN ===
TELEGRAM_TOKEN = "8664828342:AAFF12YTKx4S2qhV2Y1bmMhHJaeIPyOPhjk"
TELEGRAM_CHAT_ID = "-1003911661321"

# === TAKİP ETMEK İSTEDİĞİNİZ ANAHTAR KELİMELER ===
# Haber başlığında bu kelimelerden biri geçiyorsa haber filtrenize takılır.
ANAHTAR_KELIMELER = ["borsa", "hisse", "şirket", "alim", "satim", "anlaşma", "faiz", "fed", "bist", "endeks", "ortaklık"]

def telegram_mesaj_gonder(mesaj):
    print("Telegram mesajı gönderiliyor...")
    mesaj_kodlu = urllib.parse.quote(mesaj)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={mesaj_kodlu}"
    try:
        urllib.request.urlopen(url)
        print("Telegram mesajı başarıyla gönderildi!")
    except Exception as e:
        print(f"Telegram mesajı gönderilirken hata oldu: {e}")

def bloomberg_haberlerini_cek():
    print("Bloomberg HT haber akışına bağlanılıyor...")
    # Bloomberg HT Son Dakika Haber Akışı
    rss_url = "https://www.bloomberght.com/rss/son-dakika"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'}
    
    try:
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        filtrelenmis_haberler = []
        
        # Sitedeki tüm güncel haberleri tarıyoruz
        for item in root.findall('.//item'):
            baslik = item.find('title').text if item.find('title') is not None else ""
            link = item.find('link').text if item.find('link') is not None else ""
            
            # Başlığı küçük harfe çevirip anahtar kelimelerimizle eşleşiyor mu bakıyoruz
            baslik_kucuk = baslik.lower()
            if any(kelime in baslik_kucuk for kelime in ANAHTAR_KELIMELER):
                haber_metni = f"📰 BLOOMBERG HT\n\n🔥 {baslik}\n\nDetay: {link}"
                filtrelenmis_haberler.append(haber_metni)
                
        # Çok fazla mesaj birikmesin diye en güncel 5 tanesini seçiyoruz
        return filtrelenmis_haberler[:5]
        
    except Exception as e:
        print(f"Bloomberg haberleri çekilirken hata oluştu: {e}")
        return []

# --- Ana Programı Çalıştır ---
print("Ekonomi takip sistemi başlatıldı...")

# 1. Bloomberg'den filtreye uyan haberleri çek
guncel_haberler = bloomberg_haberlerini_cek()

# Hem dosyaya yazılacak hem ekrana basılacak metni hazırlıyoruz
dosya_metni = "=== GÜNCEL EKONOMİ VE BORSA HABERLERİ ===\n\n"

if guncel_haberler:
    print(f"{len(guncel_haberler)} adet filtrelenmiş haber bulundu.")
    for haber in guncel_haberler:
        # 2. Haberleri Telegram'a gönder
        telegram_mesaj_gonder(haber)
        # 3. Haberleri dosya metnine ekle
        dosya_metni += haber + "\n" + ("="*40) + "\n"
else:
    print("Filtrelerinize uygun yeni bir haber bulunamadı.")
    dosya_metni += "Şu an için kriterlerinize uygun yeni bir haber akışı yok.\n"

# 4. 'Gönderilenler.txt' dosyasını tamamen yeni haberlerle güncelle
with open("Gönderilenler.txt", "w", encoding="utf-8") as dosya:
    dosya.write(dosya_metni)

print("Gönderilenler.txt başarıyla güncellendi. İşlem tamam!")
