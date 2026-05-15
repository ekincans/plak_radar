import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Plak Radar Pro", layout="wide")

st.title("🛡️ Plak Radar: Merkezi Tablo")
st.write("Dükkanlardan veriler çekilerek tek bir tabloda birleştiriliyor...")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth In Cauda Venenum")

def google_search_scraping(search_query, site_domain):
    # Google üzerinden dükkan bazlı arama yapıp sonucu senin sitene döküyoruz
    search_url = f"https://www.google.com/search?q=site:{site_domain}+{search_query.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Google sonuçlarındaki ilk gerçek linki bulalım
        result = soup.select_one('div.g')
        if result:
            title = result.select_one('h3').text if result.select_one('h3') else "Ürün bulundu"
            link = result.select_one('a')['href']
            snippet = result.select_one('.VwiC3b').text if result.select_one('.VwiC3b') else ""
            
            # Snippet içinden fiyat ve stok tahmin etmeye çalışıyoruz
            stok = "Stokta Var" if "stok" in snippet.lower() or "adet" in snippet.lower() else "Kontrol Ediniz"
            if "tükendi" in snippet.lower(): stok = "Tükendi"
            
            return {"Mağaza": site_domain.replace("www.", ""), "Ürün": title, "Durum": stok, "Link": link}
    except:
        pass
    return {"Mağaza": site_domain.replace("www.", ""), "Ürün": "Bulunamadı", "Durum": "-", "Link": "#"}

if st.button("Tabloyu Hazırla"):
    if query:
        domains = ["zihni.com", "opus3a.com", "rainbow45records.com", "hammermuzik.com"]
        
        with st.spinner("Tüm dükkan verileri tek tabloda toplanıyor..."):
            all_results = []
            for site in domains:
                res = google_search_scraping(query, site)
                all_results.append(res)
            
            df = pd.DataFrame(all_results)
            
            # İşte senin istediğin tablo
            st.dataframe(
                df,
                use_container_width=True,
                column_config={
                    "Link": st.column_config.LinkColumn("Ürün Sayfası", display_text="Sayfaya Git 🔗")
                }
            )
    else:
        st.warning("Lütfen bir arama terimi girin.")
