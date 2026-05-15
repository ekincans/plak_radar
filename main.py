import streamlit as st
import pandas as pd
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Plak Radar: Multi-Tab", layout="wide")

st.title("🎯 Plak Radar: Hızlı Erişim")
st.write("Tek tıkla tüm dükkanlarda arama yapın.")

# Arama kutusu
query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth In Cauda Venenum")

def get_links(album):
    encoded_query = urllib.parse.quote(album)
    stores = [
        {"name": "Zihni Müzik", "url": f"https://www.zihni.com/arama?q={encoded_query}"},
        {"name": "Opus3a", "url": f"https://www.opus3a.com/ara?q={encoded_query}"},
        {"name": "Hammer Müzik", "url": f"https://www.hammermuzik.com/arama?q={encoded_query}"},
        {"name": "Rainbow45", "url": f"https://www.rainbow45records.com/arama?q={encoded_query}"},
        {"name": "Roll Plak", "url": f"https://www.rollplak.com/arama?q={encoded_query}"},
        {"name": "Kont Plak", "url": f"https://www.kontplak.com/search?q={encoded_query}"},
        {"name": "Discogs", "url": f"https://www.discogs.com/search/?q={encoded_query}&type=release"}
    ]
    return stores

if query:
    links_data = get_links(query)
    
    # 1. Bireysel Butonlar (Tablo Görünümü)
    st.subheader("Mağaza Linkleri")
    for item in links_data:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.write(f"**{item['name']}**")
        with col2:
            st.link_button(f"{item['name']} sayfasını aç", item['url'])

    st.divider()

    # 2. "Hepsini Aynı Anda Aç" Butonu
    st.subheader("🚀 Komando Modu")
    st.warning("⚠️ Not: Tarayıcınız sekmelerin açılmasını engellerse, adres çubuğunun sağındaki 'Pop-up engelleyici' ikonuna tıklayıp bu siteye izin verin.")
    
    if st.button("Tüm Mağazaları Yeni Sekmelerde Aç"):
        # JavaScript ile tüm linkleri tek tek açma komutu
        js_code = "".join([f"window.open('{item['url']}', '_blank');" for item in links_data])
        components.html(f"<script>{js_code}</script>", height=0)
        st.success("Tüm sekmeler tetiklendi!")

else:
    st.info("Aramak istediğin albümü yazınca dükkan linkleri burada belirecek.")
