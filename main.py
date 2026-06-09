import urllib.request
import xml.etree.ElementTree as ET

def kap_haberlerini_cek():
    print("KAP sitesine bağlanılıyor...")
    # KAP'ın resmi güncel duyuru akışı adresi
    rss_url = "https://www.kap.org.tr/tr/api/disclosures"
    
    try:
        # Siteye bağlanıp veriyi indiriyoruz
        with urllib.request.urlopen(rss_url) as response:
            xml_data = response.read()
            
        # Gelen veriyi bilgisayarın anlayacağı dile çeviriyoruz
        root = ET.fromstring(xml_data)
        
        haberler = []
        # En güncel 5 haberi ayıklıyoruz
        for item in root.findall('.//item')[:5]:
            baslik = item.find('title').text if item.find('title') is not None else "Başlık Yok"
            link = item.find('link').text if item.find('link') is not None else ""
            tarih = item.find('pubDate').text if item.find('pubDate') is not None else ""
            
            haber_metni = f"Zaman: {tarih}\nHaber: {baslik}\nDetay: {link}\n{'-'*50}\n"
            haberler.append(haber_metni)
            
        return "".join(haberler)
        
    except Exception as e:
        return f"KAP haberleri çekilirken bir hata oluştu: {e}\n"

# --- Sizin Mevcut Dosya Oluşturma Kısmınız ---
print("Gönderilenler dosyası hazırlanıyor...")

# KAP haberlerini çekiyoruz
guncel_kap_haberleri = kap_haberlerini_cek()

# Hepsini 'Gönderilenler.txt' dosyasına kaydediyoruz
with open("Gönderilenler.txt", "w", encoding="utf-8") as dosya:
    dosya.write("=== GÜNCEL KAP HABERLERİ ===\n\n")
    dosya.write(guncel_kap_haberleri)
    dosya.write("\n=== İşlem Başarıyla Tamamlandı ===")

print("Gönderilenler dosyası oluştu ve KAP haberleri eklendi!")
