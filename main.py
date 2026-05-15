import streamlit as st
import pandas as pd
import requests

# Secrets üzerinden çekiyoruz (Güvenli yöntem)
API_KEY = st.secrets["GOOGLE_API_KEY"] 
CX = "a7ad9ddff557f4f93"

st.set_page_config(page_title="Plak Radar", layout="wide")

st.title("🛡️ Plak Radar: Merkezi Tablo")
st.write("Google API üzerinden dükkan stokları taranıyor...")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def google_api_search(search_query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": API_KEY,
        "cx": CX,
        "q": search_query,
        "hl": "tr"
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()
        
        # Hata varsa ekrana bas (Burası sorunu çözecek)
        if "error" in data:
            st.error(f"Google Hatası: {data['error']['message']}")
            return []

        results = []
        if "items" in data:
            for item in data["items"]:
                # ... (geri kalan kod aynı kalsın)
                site_name = item["displayLink"].replace("www.", "")
                title = item["title"]
                link = item["link"]
                snippet = item.get("snippet", "").lower()
                stok = "🔴 Tükendi" if "tükendi" in snippet or "stokta yok" in snippet else "🟢 Stokta"
                results.append({"Mağaza": site_name, "Ürün": title, "Durum": stok, "Link": link})
            return results
    except Exception as e:
        st.error(f"API Hatası: {e}")
    return []

if st.button("Tabloyu Hazırla"):
    if query:
        with st.spinner(f"'{query}' taranıyor..."):
            results = google_api_search(query)
            if results:
                df = pd.DataFrame(results).drop_duplicates(subset=['Mağaza'])
                st.dataframe(df, use_container_width=True, column_config={
                    "Link": st.column_config.LinkColumn("Ürün Sayfası", display_text="Dükkana Git 🛒")
                })
            else:
                st.info("Sonuç bulunamadı.")
    else:
        st.warning("Bir isim girin.")
