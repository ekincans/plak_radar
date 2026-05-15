import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Plak Radar", page_icon=" vinyl", layout="wide")

st.title("🛡️ Plak Radar")
st.write("Zihni.com ve Opus3a stoklarını anlık tarar.")

query = st.text_input("Aradığınız Plak:", placeholder="Örn: Led Zeppelin IV")

# Daha güçlü bir kimlik bilgisi
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def scrape_zihni(query):
    try:
        # Yeni güncel adres: zihni.com
        url = f"https://www.zihni.com/arama?q={query.replace(' ', '+')}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # Ürün kutusunu bulalım
        item = soup.select_one(".product-item")
        if item:
            name = item.select_one(".product-title").text.strip()
            price = item.select_one(".product-price").text.strip()
            # Stok kontrolü: "Tükendi" ibaresi yoksa stokta varsayıyoruz
            stok = "Tükendi" if "tükendi" in item.text.lower() else "Stokta"
            return {"Mağaza": "Zihni Müzik", "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
    except Exception as e:
        return {"Mağaza": "Zihni Müzik", "Ürün": "Hata oluştu", "Fiyat": "-", "Durum": "Erişim Sorunu", "Link": url}
    return {"Mağaza": "Zihni Müzik", "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": url}

def scrape_opus3a(query):
    try:
        url = f"https://www.opus3a.com/arama?q={query.replace(' ', '+')}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.content, "html.parser")
        
        item = soup.select_one(".product-item")
        if item:
            name = item.select_one(".product-item-title").text.strip()
            price = item.select_one(".product-item-price").text.strip()
            # Sepete ekle butonu varsa stokta demektir
            stok = "Stokta" if item.select_one(".add-to-cart") else "Tükendi"
            return {"Mağaza": "Opus3a", "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
    except Exception as e:
        return {"Mağaza": "Opus3a", "Ürün": "Hata oluştu", "Fiyat": "-", "Durum": "Erişim Sorunu", "Link": url}
    return {"Mağaza": "Opus3a", "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": url}

if st.button("Plağı Ara"):
    if query:
        with st.spinner(f"'{query}' aranıyor..."):
            results = [scrape_zihni(query), scrape_opus3a(query)]
            
            df = pd.DataFrame(results)
            # Sonuçları göster
            st.dataframe(df, use_container_width=True, column_config={
                "Link": st.column_config.LinkColumn("Mağazaya Git")
            })
    else:
        st.warning("Lütfen bir plak adı girin.")
