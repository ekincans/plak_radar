import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Plak Radar: Dashboard", layout="wide")

st.title("🎯 Plak Radar: Hızlı Erişim")
st.write("Dükkanların bot korumasına takılmadan, doğrudan arama sayfalarına gidin.")

# Arama kutusu
query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Blackwater Park")

def generate_search_links(album):
    # Dükkan isimleri ve arama linki yapıları
    encoded_query = urllib.parse.quote(album)
    
    stores = [
        {"Mağaza": "Zihni Müzik", "URL": f"https://www.zihni.com/arama?q={encoded_query}"},
        {"Mağaza": "Opus3a", "URL": f"https://www.opus3a.com/arama?q={encoded_query}"},
        {"Mağaza": "Hammer Müzik", "URL": f"https://www.hammermuzik.com/arama?q={encoded_query}"},
        {"Mağaza": "Rainbow45", "URL": f"https://www.rainbow45records.com/arama?q={encoded_query}"},
        {"Mağaza": "Roll Plak", "URL": f"https://www.rollplak.com/arama?q={encoded_query}"},
        {"Mağaza": "Kont Plak", "URL": f"https://www.kontplak.com/search?q={encoded_query}"},
        {"Mağaza": "Discogs (Global)", "URL": f"https://www.discogs.com/search/?q={encoded_query}&type=release"}
    ]
    return stores

if query:
    st.subheader(f"'{query}' için Hazırlanan Linkler")
    links = generate_search_links(query)
    
    # Şık bir tablo ve butonlar
    for link in links:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"**")
        with col2:
            st.link_button(f"{link['Mağaza']} dükkanında ara 🔍", link['URL'])
    
    st.divider()
    st.info("💡 Yukarıdaki butonlara bastığında dükkanın arama sonuçları yeni sekmede açılır. Bot korumasına takılmazsın çünkü aramayı dükkanın kendi sitesinde yapmış olursun.")

else:
    st.info("Aramak istediğin albüm veya sanatçı ismini yukarıya yaz.")
