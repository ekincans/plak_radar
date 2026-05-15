import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Plak Radar", layout="wide")

st.title("🎯 Plak Radar")

# Arama Kutusu
query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def get_links_dict(album):
    """Mağazaları isim-url ikilisi olarak bir sözlükte tutalım"""
    encoded_query = urllib.parse.quote(album)
    return {
        "Roll Plak": f"https://rollplak.com/index.php?route=product/search&search={encoded_query}&description=true",
        "Plak Sepeti": f"https://www.plaksepeti.com.tr/arama/{encoded_query}?stockOnly=1&sort=",
        "Plak Burada": f"https://www.plakburada.com/arama/{encoded_query}?stockOnly=1&sort=",
        "CD Plak": f"https://cdplak.com/index.php?route=product/search&search={encoded_query}&ff3=11&fq=1",
        "Rainbow45": f"https://www.rainbow45records.com/Arama?kelime={encoded_query}",
        "Zihni Müzik": f"https://www.zihni.com/arama/{encoded_query}",
        "Alp Plak": f"https://www.alpplak.com/index.php?route=product/search&search={encoded_query}&description=true&fq=1",
        "Ege Kitabevi": f"https://egekitabevi.net/?s={encoded_query}&post_type=product",
        "Opus3a": f"https://www.opus3a.com/ara?q={encoded_query}&filtre=is:1;pfor:Plak",
        "Atlantis": f"https://www.atlantismusicshop.com/index.php?route=product/search&search={encoded_query}",
        "Hammer": f"https://www.hammeronlineshop.com/search?p=Products&q_field_active=0&ctg_id=&q={encoded_query}&search=&q_field=",
        "TLPMA": f"https://tlpma.com.tr/shop/?s={encoded_query}&post_type=product&stock_status=instock,onsale",
        "Plak İstasyonu": f"https://www.plakistasyonu.com/arama/{encoded_query}?stockOnly=1&sort=",
        "Pera Plak": f"https://www.peraplak.com/arama/{encoded_query}?stockOnly=1&sort=",
        "Beat Sommelier": f"https://www.beatsommelier.com/search?q={encoded_query}&sort_by=relevance&filter.v.availability=1"
    }

if query:
    all_links = get_links_dict(query)
    store_names = list(all_links.keys())

    # --- Mağaza Seçim Alanı ---
    st.write("---")
    selected_stores = st.multiselect(
        "Arama yapılacak mağazaları seçin:",
        options=store_names,
        default=store_names # Başlangıçta hepsi seçili gelsin
    )

    # --- Butonlar ---
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 SEÇİLİ MAĞAZALARI AÇ", use_container_width=True):
            if selected_stores:
                # Sadece seçilen mağazaların URL'lerini JS'e gönderiyoruz
                js_code = "".join([f"window.open('{all_links[s]}', '_blank');" for s in selected_stores])
                components.html(f"<script>{js_code}</script>", height=0)
                st.toast(f"{len(selected_stores)} mağaza açılıyor...")
            else:
                st.warning("Lütfen en az bir mağaza seçin.")

    with col2:
        if st.button("🗑️ SEÇİMİ TEMİZLE", use_container_width=True):
            # Streamlit'in doğası gereği bu buton sayfayı yenileyerek seçimleri sıfırlar
            st.rerun()

    # --- Alt Kısım: Seçili Mağazaların Bireysel Butonları ---
    if selected_stores:
        st.write(f"### Seçili Mağazalar ({len(selected_stores)})")
        cols = st.columns(5)
        for idx, store in enumerate(selected_stores):
            with cols[idx % 5]:
                st.link_button(store, all_links[store], use_container_width=True)
    
    st.write("---")
    st.caption("Pop-up engelleyiciyi kapatmayı unutmayın.")

else:
    st.info("Albüm ismini yazarak başlayın.")
