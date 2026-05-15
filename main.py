import streamlit as st
import pandas as pd
import requests

# --- AYARLAR ---
# API Key'i aldıktan sonra tırnak içine yapıştır
API_KEY = "AIzaSyDmLEx8zge0VpgVGAMTxXrj-SnihraHCTU" 
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
        
        results = []
        if "items" in data:
            for item in data["items"]:
                # Site adını temizleyelim
                site_name = item["displayLink"].replace("www.", "")
                
                # Başlık ve Link
                title = item["title"]
                link = item["link"]
                
                # Stok durumunu açıklamadan tahmin edelim
                snippet = item.get("snippet", "").lower()
                stok = "Stokta Var"
                if "tükendi" in snippet or "stokta yok" in snippet:
                    stok = "🔴 Tükendi"
                else:
                    stok = "🟢 Stokta"
                
                results.append({
                    "Mağaza": site_name,
                    "Ürün": title,
                    "Durum": stok,
                    "Link": link
                })
            return results
    except Exception as e:
        st.error(f"API Hatası: {e}")
    return []

if st.button("Tabloyu Hazırla"):
    if API_KEY == "AIzaSyDmLEx8zge0VpgVGAMTxXrj-SnihraHCTU":
        st.error("Lütfen önce API Key'inizi koda ekleyin!")
    elif query:
        with st.spinner(f"'{query}' için tüm dükkanlar taranıyor..."):
            results = google_api_search(query)
            
            if results:
                df = pd.DataFrame(results)
                # Aynı mağazadan birden fazla sonuç gelirse en üsttekini tutalım
                df = df.drop_duplicates(subset=['Mağaza'])
                
                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "Link": st.column_config.LinkColumn("Ürün Sayfası", display_text="Dükkana Git 🛒")
                    }
                )
            else:
                st.info("Sonuç bulunamadı. Aramayı biraz daha detaylandırabilirsin.")
    else:
        st.warning("Bir isim girin.")
