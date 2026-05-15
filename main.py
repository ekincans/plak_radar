import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Plak Radar", page_icon=" vinyl", layout="wide")

# Görsel düzenlemeler
st.markdown("""
    <style>
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Plak Radar")
st.write("Dükkanlarda anlık arama yapın:")

query = st.text_input("Plak / Sanatçı Adı:", placeholder="Örn: Pink Floyd - Animals")

# En üst düzey tarayıcı kimliği (Sitenin bizi insan sanması için)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def scrape_engine(store_name, url, selectors):
    try:
        # Siteye isteği gönderiyoruz
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        # Eğer site bizi engellediyse (403 veya 404 hatası)
        if response.status_code != 200:
            return {"Mağaza": store_name, "Sonuç": "Erişim Engellendi", "Fiyat": "-", "Durum": "Linkten Bakınız", "Link": url}

        soup = BeautifulSoup(response.content, "html.parser")
        
        # Ürün kutusunu bulmaya çalışalım
        item = soup.select_one(selectors['item'])
        if item:
            name = item.select_one(selectors['title']).text.strip() if item.select_one(selectors['title']) else "Bilinmiyor"
            price = item.select_one(selectors['price']).text.strip() if item.select_one(selectors['price']) else "-"
            stok = "Tükendi" if "tükendi" in item.text.lower() or "stokta yok" in item.text.lower() else "Stokta Var"
            return {"Mağaza": store_name, "Sonuç": name, "Fiyat": price, "Durum": stok, "Link": url}
            
    except Exception as e:
        pass
    
    # Hiçbir şey bulunamazsa en azından çalışan linki döndür
    return {"Mağaza": store_name, "Sonuç": "Mağazada Ara 🔍", "Fiyat": "-", "Durum": "Linke Tıklayın", "Link": url}

if st.button("Tüm Dükkanları Tara"):
    if query:
        search_term = query.replace(" ", "+")
        
        # Mağaza Ayarları (Senin düzelttiğin linklerle)
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
            }
        ]
        
        with st.spinner("Dükkanlar taranıyor..."):
            results = []
            for store in stores:
                res = scrape_engine(store['name'], store['url'], store['selectors'])
                results.append(res)
            
            df = pd.DataFrame(results)
            
            # Tabloyu şık bir şekilde gösteriyoruz
            st.dataframe(df, use_container_width=True, column_config={
                "Link": st.column_config.LinkColumn("Mağaza Sayfasını Aç")
            })
    else:
        st.error("Lütfen bir isim yazın.")
