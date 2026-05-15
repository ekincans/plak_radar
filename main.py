import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

st.set_page_config(page_title="Plak Radar", page_icon=" vinyl", layout="wide")

st.title("🛡️ Plak Radar")
st.write("Dükkanlardan canlı fiyat ve stok bilgisi çekiliyor...")

query = st.text_input("Aradığınız Albüm / Sanatçı:", placeholder="Örn: Camel - Moonmadness")

def get_data(store_name, search_url, selectors):
    # Her mağaza için yeni bir oturum simüle ediyoruz
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/" # Google üzerinden gelmiş gibi yapıyoruz
    }
    
    try:
        response = session.get(search_url, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"Mağaza": store_name, "Ürün": "Erişim Sorunu (403)", "Fiyat": "-", "Stok": "Engellendi", "Link": search_url}
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # İlk ürünü bulma
        item = soup.select_one(selectors['item'])
        if item:
            # Ürün Adı
            title_el = item.select_one(selectors['title'])
            name = title_el.text.strip() if title_el else "İsim çekilemedi"
            
            # Fiyat
            price_el = item.select_one(selectors['price'])
            price = price_el.text.strip() if price_el else "Fiyat yok"
            
            # Stok (Mantık: 'Tükendi' yazısı yoksa veya 'Sepete Ekle' varsa stoktadır)
            item_text = item.get_text().lower()
            if "tükendi" in item_text or "stokta yok" in item_text or "out of stock" in item_text:
                stok_durumu = "🔴 Tükendi"
            else:
                stok_durumu = "🟢 Stokta"
            
            # Ürünün kendi satış linkini çekmeye çalışalım
            link_el = item.select_one("a")
            final_link = search_url # Varsayılan arama linki
            if link_el and link_el.get('href'):
                href = link_el.get('href')
                if href.startswith("http"):
                    final_link = href
                else:
                    # Göreli linkleri ( /urun/123 ) tam linke çeviriyoruz
                    base_url = "https://" + search_url.split("/")[2]
                    final_link = base_url + href

            return {"Mağaza": store_name, "Ürün": name, "Fiyat": price, "Stok": stok_durumu, "Link": final_link}
        
        return {"Mağaza": store_name, "Ürün": "Bulunamadı", "Fiyat": "-", "Stok": "-", "Link": search_url}
        
    except Exception as e:
        return {"Mağaza": store_name, "Ürün": "Hata", "Fiyat": "-", "Stok": "Bağlantı Hatası", "Link": search_url}

if st.button("Radarı Çalıştır"):
    if query:
        search_term = query.replace(" ", "+")
        
        stores = [
            {
                "name": "Zihni Müzik",
                "url": f"https://www.zihni.com/arama/{search_term}",
                "selectors": {"item": ".product-item", "title": ".product-title", "price": ".product-price"}
            },
            {
                "name": "Opus3a",
                "url": f"https://www.opus3a.com/ara?q={search_term}",
                "selectors": {"item": ".product-item", "title": ".product-item-title", "price": ".product-item-price"}
            },
            {
                "name": "Rainbow45",
                "url": f"https://www.rainbow45records.com/arama?q={search_term}",
                "selectors": {"item": ".product-item", "title": ".product-title", "price": ".product-price"}
            }
        ]
        
        with st.spinner("Plak dükkanları taranıyor..."):
            results = []
            for store in stores:
                results.append(get_data(store['name'], store['url'], store['selectors']))
                time.sleep(1) # Siteleri yormamak ve banlanmamak için kısa ara
            
            df = pd.DataFrame(results)
            
            # Tabloyu göster (Linkler tıklanabilir olacak)
            st.dataframe(
                df, 
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn("Satış Sayfasına Git", display_text="Satın Al 🛒")
                }
            )
    else:
        st.warning("Lütfen bir plak veya sanatçı adı yazın.")
