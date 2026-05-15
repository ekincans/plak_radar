import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Plak Radar", layout="wide")

# Başlık ve Açıklama
st.title("🎯 Plak Radar")

# Arama Kutusu
query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def get_links(album):
    encoded_query = urllib.parse.quote(album)
    return [
        {"name": "Zihni", "url": f"https://www.zihni.com/arama?q={encoded_query}"},
        {"name": "Opus3a", "url": f"https://www.opus3a.com/arama?q={encoded_query}"},
        {"name": "Hammer", "url": f"https://www.hammermuzik.com/arama?q={encoded_query}"},
        {"name": "Rainbow45", "url": f"https://www.rainbow45records.com/arama?q={encoded_query}"},
        {"name": "Roll Plak", "url": f"https://www.rollplak.com/arama?q={encoded_query}"},
        {"name": "Kont Plak", "url": f"https://www.kontplak.com/search?q={encoded_query}"},
        {"name": "Discogs", "url": f"https://www.discogs.com/search/?q={encoded_query}&type=release"}
    ]

if query:
    links_data = get_links(query)
    
    # --- Üst Kısım: Hepsini Aç Butonu ---
    st.write("---")
    col_main, _ = st.columns([1, 2]) # Butonu sola yaslamak için
    with col_main:
        if st.button("🚀 TÜM DÜKKANLARI AYNI ANDA AÇ", use_container_width=True):
            js_code = "".join([f"window.open('{item['url']}', '_blank');" for item in links_data])
            components.html(f"<script>{js_code}</script>", height=0)
            st.toast("Sekmeler tetiklendi! Engellendiyse pop-up izni verin.")

    # --- Orta Kısım: Kompakt Buton Izgarası ---
    st.write("### Mağazalar")
    
    # Butonları 4'lü sütunlar halinde dizelim (Daha kompakt görünüm)
    cols = st.columns(4)
    for idx, item in enumerate(links_data):
        with cols[idx % 4]:
            st.link_button(item['name'], item['url'], use_container_width=True)

    st.write("---")
    st.caption("Not: Tarayıcı pop-up engelleyicisi uyarısı verirse 'Her zaman izin ver' demeyi unutmayın.")

else:
    st.info("Aramak istediğin plağı yaz, dükkanlar saniyeler içinde karşında olsun.")
