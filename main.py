import urllib.request
import xml.etree.ElementTree as ET

# === TELEGRAM BİLGİLERİNİZİ BURAYA YAZIN ===
TELEGRAM_TOKEN = "TOKEN_BURAYA"
TELEGRAM_CHAT_ID = "CHAT_ID_BURAYA"

def telegram_mesaj_gonder(mesaj):
    print("Telegram mesajı gönderiliyor...")
    mesaj_kodlu = urllib.parse.quote(mesaj)
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={mesaj_kodlu}"
    try:
        urllib.request.urlopen(url)
        print("Telegram mesajı başarıyla gönderildi!")
    except Exception as e:
        print(f"Telegram mesajı gönderilirken hata oldu: {e}")

def kap_haberlerini_cek():
    print("KAP sitesine bağlanılıyor...")
    rss_url = "https://www.kap.org.tr/tr/api/disclosures"
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15'}
    
    try:
        req = urllib.request.Request(rss_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        haberler = []
        # En güncel 3 haberi alıyoruz
        for item in root.findall('.//item')[:3]:
            baslik = item.find('title').text if item.find('title') is not None else "Başlık Yok"
            link = item.find('link').text if item.find('link') is not None else ""
            
            haber_metni = f"🔔 KAP HABERİ\n\n{baslik}\n\nDetay: {link}"
            haberler.append(haber_metni)
            
        return haberler
    except Exception as e:
        print(f"KAP çekilirken hata oluştu: {e}")
        return []

# --- Sistemi Çalıştır ---
guncel_haberler = kap_haberlerini_cek()

# Hem dosyaya yazacağımız hem Telegram'a atacağımız metni hazırlıyoruz
dosya_metni = "=== GÜNCEL KAP HABERLERİ ===\n\n"

if guncel_haberler:
    for haber in guncel_haberler:
        # 1. Telegram'a gönder
        telegram_mesaj_gonder(haber)
        # 2. Dosya metnine ekle
        dosya_metni += haber + "\n" + ("-"*30) + "\n"
else:
    dosya_metni += "Haber bulunamadı veya bir hata oluştu."

# 3. 'Gönderilenler.txt' dosyasını tamamen yeni haberlerle güncelle
with open("Gönderilenler.txt", "w", encoding="utf-8") as dosya:
    dosya.write(dosya_metni)

print("Dosya güncellendi ve işlem bitti!")
