import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

st.set_page_config(page_title="Plak Radar", page_icon=" vinyl", layout="wide")
st.title("🛡️ Plak Radar")

query = st.text_input("Aradığınız Plak:", placeholder="Örn: Pink Floyd Animals")

# En güncel tarayıcı taklidi
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def search_site(store_name, url, item_selector, title_selector, price_selector):
    try:
        # Siteye gitmeden önce çok kısa bir bekleme (bot koruması için)
        time.sleep(1)
        r = requests.get(url, headers=HEADERS, timeout=20)
        
        if r.status_code != 200:
            return {"Mağaza": store_name, "Ürün": "Erişim Engellendi", "Fiyat": "-", "Durum": f"Hata {r.status_code}", "Link": url}
        
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Ürünü bulma
        item = soup.select_one(item_selector)
        if item:
            name = item.select_one(title_selector).text.strip() if item.select_one(title_selector) else "İsim bulunamadı"
            price = item.select_one(price_selector).text.strip() if item.select_one(price_selector) else "Fiyat yok"
            stok = "Tükendi" if "tükendi" in item.text.lower() or "stokta yok" in item.text.lower() else "Stokta"
            return {"Mağaza": store_name, "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
            
    except Exception as e:
        return {"Mağaza": store_name, "Ürün": "Hata", "Fiyat": "-", "Durum": str(e)[:15], "Link": url}
    
    return {"Mağaza": store_name, "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": url}

if st.button("Plağı Ara"):
    if query:
        with st.spinner("Dükkanlar taranıyor..."):
            # Arama terimini URL formatına çeviriyoruz
            search_term = query.replace(" ", "+")
            
            # Her site için güncel kod yapıları
            results = [
                search_site("Zihni Müzik", f"https://www.zihni.com/arama/{search_term}", ".product-item", ".product-title", ".product-price"),
                search_site("Opus3a", f"https://www.opus3a.com/ara?q={search_term}", ".product-item", ".product-item-title", ".product-item-price")
            ]
            
            df = pd.DataFrame(results)
            st.table(df)
    else:
        st.warning("Lütfen bir isim girin.")
