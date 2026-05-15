import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

st.set_page_config(page_title="Plak Radar: Yerli ve Milli", layout="wide")

st.title("📦 Plak Radar: Doğrudan Arama")
st.write("Arama motorlarını aradan çıkardık, dükkanlara doğrudan bağlanıyoruz.")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def dukkan_tara(site_url, search_path, query):
    # Gerçek bir tarayıcı gibi görünmek için en kritik parça:
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Mobile/15E148 Safari/604.1",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    # Boşlukları dükkanın istediği formatta (+ veya %20) değiştiriyoruz
    formatted_query = query.replace(" ", "+")
    full_url = f"{site_url}{search_path}{formatted_query}"
    
    try:
        response = requests.get(full_url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            return soup, full_url
    except:
        pass
    return None, full_url

def sonuclari_ayikla(dukkan_adi, soup, full_url):
    # Her dükkanın sayfa yapısı farklı olduğu için burayı özelleştiriyoruz
    try:
        if "opus3a" in dukkan_adi:
            # Opus3a için ilk ürünü bulma mantığı
            item = soup.select_one(".product-item")
            if item:
                title = item.select_one(".product-title").text.strip()
                price = item.select_one(".product-price").text.strip()
                return {"Mağaza": "Opus3a", "Ürün": title, "Fiyat": price, "Link": full_url}
        
        elif "zihni" in dukkan_adi:
            item = soup.select_one(".productItem")
            if item:
                title = item.select_one(".productName").text.strip()
                price = item.select_one(".productPrice").text.strip()
                return {"Mağaza": "Zihni Müzik", "Ürün": title, "Fiyat": price, "Link": full_url}
        
        elif "hammer" in dukkan_adi:
            item = soup.select_one(".product-list-item")
            if item:
                title = item.select_one(".product-title").text.strip()
                return {"Mağaza": "Hammer Müzik", "Ürün": title, "Fiyat": "Bakınız", "Link": full_url}
    except:
        pass
    return None

if st.button("Tabloyu Oluştur"):
    if query:
        # Taranacak dükkan listesi ve arama yolları
        targets = [
            {"name": "opus3a", "base": "https://www.opus3a.com", "path": "/arama?q="},
            {"name": "zihni", "base": "https://www.zihni.com", "path": "/arama?q="},
            {"name": "hammer", "base": "https://www.hammermuzik.com", "path": "/arama?q="}
        ]
        
        results = []
        with st.spinner("Dükkan dükkan geziliyor..."):
            for t in targets:
                soup, link = dukkan_tara(t["base"], t["path"], query)
                if soup:
                    res = sonuclari_ayikla(t["name"], soup, link)
                    if res:
                        results.append(res)
                time.sleep(1) # Banlanmamak için kısa bir bekleme
            
            if results:
                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)
                st.success("Sonuçlar dükkanların kendi sistemlerinden çekildi!")
            else:
                st.error("Dükkanlar şu an yanıt vermiyor veya ürün bulunamadı. Lütfen farklı bir albüm dene.")
    else:
        st.warning("Arama terimi girilmedi.")
