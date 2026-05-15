import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Plak Radar", layout="wide")

st.title("🎯 Plak Radar")

# Arama Kutusu
query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def get_links(album):
    encoded_query = urllib.parse.quote(album)
    # Senin gönderdiğin linklerin dinamik versiyonları
    return [
        {"name": "Roll Plak", "url": f"https://rollplak.com/index.php?route=product/search&search={encoded_query}&description=true"},
        {"name": "Plak Sepeti", "url": f"https://www.plaksepeti.com.tr/arama/{encoded_query}?stockOnly=1&sort="},
        {"name": "Plak Burada", "url": f"https://www.plakburada.com/arama/{encoded_query}?stockOnly=1&sort="},
        {"name": "CD Plak", "url": f"https://cdplak.com/index.php?route=product/search&search={encoded_query}&ff3=11&fq=1"},
        {"name": "Rainbow45", "url": f"https://www.rainbow45records.com/Arama?kelime={encoded_query}"},
        {"name": "Zihni Müzik", "url": f"https://www.zihni.com/arama/{encoded_query}"},
        {"name": "Alp Plak", "url": f"https://www.alpplak.com/index.php?route=product/search&search={encoded_query}&description=true&fq=1"},
        {"name": "Ege Kitabevi", "url": f"https://egekitabevi.net/?s={encoded_query}&post_type=product"},
        {"name": "Opus3a", "url": f"https://www.opus3a.com/ara?q={encoded_query}&filtre=is:1;pfor:Plak"},
        {"name": "Atlantis", "url": f"https://www.atlantismusicshop.com/index.php?route=product/search&search={encoded_query}"},
        {"name": "Hammer", "url": f"https://www.hammeronlineshop.com/search?p=Products&q_field_active=0&ctg_id=&q={encoded_query}&search=&q_field="},
        {"name": "TLPMA", "url": f"https://tlpma.com.tr/shop/?s={encoded_query}&post_type=product&stock_status=instock,onsale"},
        {"name": "Plak İstasyonu", "url": f"https://www.plakistasyonu.com/arama/{encoded_query}?stockOnly=1&sort="},
        {"name": "Pera Plak", "url": f"https://www.peraplak.com/arama/{encoded_query}?stockOnly=1&sort="},
        {"name": "Beat Sommelier", "url": f"https://www.beatsommelier.com/search?q={encoded_query}&sort_by=relevance&filter.v.availability=1"}
    ]

if query:
    links_data = get_links(query)
    
    # --- Üst Kısım: Hepsini Aç Butonu ---
    st.write("---")
    col_main, _ = st.columns([1, 2])
    with col_main:
        # Butona basıldığında JS ile tüm linkleri tetikler
        if st.button("🚀 TÜM DÜKKANLARI AYNI ANDA AÇ", use_container_width=True):
            js_code = "".join([f"window.open('{item['url']}', '_blank');" for item in links_data])
            components.html(f"<script>{js_code}</script>", height=0)
            st.toast(f"{len(links_data)} mağaza için sekmeler açılıyor...")

    # --- Orta Kısım: Kompakt Buton Izgarası ---
    st.write(f"### Mağazalar ({len(links_data)})")
    
    # 5'li grid yaparak daha da kompakt hale getirdik
    cols = st.columns(5)
    for idx, item in enumerate(links_data):
        with cols[idx % 5]:
            st.link_button(item['name'], item['url'], use_container_width=True)

    st.write("---")
    st.caption("Arama sonuçları yeni sekmede açılır. Pop-up engelleyiciyi kapatmayı unutma.")

else:
    st.info("Albüm ismini yazıp Enter'a bas, dükkanlar listelensin.")
