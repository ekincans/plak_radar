import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Sayfa Ayarları
st.set_page_config(page_title="Plak Radar", page_icon=" vinyl", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ Plak Radar")
st.write("Opus3a, Zihni Müzik ve Rainbow45 stoklarını anlık tarar.")

query = st.text_input("Aradığınız Plak veya Sanatçı:", placeholder="Örn: Pink Floyd Animals")

def scrape_opus3a(query):
    try:
        url = f"https://www.opus3a.com/arama?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        # İlk ürünü bulmaya çalışalım
        item = soup.find("div", class_="product-item")
        if item:
            name = item.find("div", class_="product-item-title").text.strip()
            price = item.find("div", class_="product-item-price").text.strip()
            # Stok kontrolü (Sepete ekle butonu var mı?)
            stok = "Stokta" if item.find("a", class_="add-to-cart") else "Tükendi"
            return {"Mağaza": "Opus3a", "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
    except:
        pass
    return {"Mağaza": "Opus3a", "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": "https://www.opus3a.com"}

def scrape_zihni(query):
    try:
        url = f"https://www.zihnizihni.com/arama?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        item = soup.find("div", class_="product-item")
        if item:
            name = item.find("a", class_="product-title").text.strip()
            price = item.find("div", class_="product-price").text.strip()
            stok = "Stokta" if "Sepete Ekle" in item.text else "Tükendi"
            return {"Mağaza": "Zihni Müzik", "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
    except:
        pass
    return {"Mağaza": "Zihni Müzik", "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": "https://www.zihnizihni.com"}

def scrape_rainbow45(query):
    try:
        url = f"https://www.rainbow45records.com/arama?q={query.replace(' ', '+')}"
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")
        
        item = soup.find("div", class_="product-item")
        if item:
            name = item.find("div", class_="product-title").text.strip()
            price = item.find("div", class_="product-price").text.strip()
            stok = "Stokta" if "Sepete Ekle" in item.text else "Tükendi"
            return {"Mağaza": "Rainbow45", "Ürün": name, "Fiyat": price, "Durum": stok, "Link": url}
    except:
        pass
    return {"Mağaza": "Rainbow45", "Ürün": "Bulunamadı", "Fiyat": "-", "Durum": "-", "Link": "https://www.rainbow45records.com"}

if st.button("Plağı Ara"):
    if query:
        with st.spinner("Dükkanlar taranıyor..."):
            results = [
                scrape_opus3a(query),
                scrape_zihni(query),
                scrape_rainbow45(query)
            ]
            
            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True, column_config={
                "Link": st.column_config.LinkColumn("Mağazaya Git")
            })
    else:
        st.error("Lütfen bir isim yazın.")
