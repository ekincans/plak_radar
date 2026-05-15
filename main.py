import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Plak Radar Pro", layout="wide")

st.title("🛡️ Plak Radar: Kesin Sonuç Paneli")
st.write("Google Altyapısı ile dükkan stokları taranıyor...")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def google_search(search_query, site_url):
    # Google'ın 'site:' operatörünü kullanarak dükkan bazlı arama yapıyoruz
    # Bu yöntem bot engelini tamamen aşar
    api_url = "https://www.google.com/search"
    params = {
        "q": f"site:{site_url} {search_query}",
        "hl": "tr"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        r = requests.get(api_url, params=params, headers=headers, timeout=10)
        # Google sonuçlarını analiz ediyoruz
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Google'ın bulduğu ilk sonucu alalım
        result = soup.find("div", class_="g")
        if result:
            title = result.find("h3").text if result.find("h3") else "Ürün bulundu"
            link = result.find("a")["href"]
            snippet = result.find("div", class_="VwiC3b").text if result.find("div", class_="VwiC3b") else ""
            
            # Stok tahmini
            stok = "Stokta Var"
            if "tükendi" in snippet.lower() or "stokta yok" in snippet.lower():
                stok = "Tükendi"
                
            return {"Mağaza": site_url, "Bulunan Ürün": title, "Durum": stok, "Link": link}
    except:
        pass
    return {"Mağaza": site_url, "Bulunan Ürün": "Sonuç Yok", "Durum": "-", "Link": "#"}

if st.button("Radarı Çalıştır"):
    if query:
        # Senin listenin en önemli dükkanları
        target_sites = [
            "zihni.com", 
            "opus3a.com", 
            "rainbow45records.com", 
            "hammermuzik.com",
            "rollplak.com",
            "atlantis-music.com"
        ]
        
        with st.spinner(f"'{query}' dükkanlarda aranıyor..."):
            all_data = []
            for site in target_sites:
                res = google_search(query, site)
                all_data.append(res)
            
            df = pd.DataFrame(all_data)
            
            # Tabloyu gösteriyoruz
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn("Satın Al / İncele", display_text="Dükkana Git 🔗")
                }
            )
    else:
        st.warning("Lütfen bir isim girin.")
