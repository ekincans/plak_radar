import streamlit as st
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Plak Radar", layout="wide")

# Özel CSS: Seçilen mağazaların kutularını renklendirmek için
st.markdown("""
    <style>
    .stCheckbox {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid #d1d5db;
        transition: 0.3s;
    }
    .stCheckbox:hover {
        border-color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎯 Plak Radar")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Damnation")

def get_links_dict(album):
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
    
    # --- Üst Kontrol Butonları ---
    st.write("---")
    col_btn1, col_btn2 = st.columns(2)
    
    selected_stores = [] # Seçilenleri burada tutacağız

    with col_btn1:
        # Bu buton sadece grid'den işaretlediğin mağazaları açar
        btn_selected = st.button("🚀 SEÇİLİ MAĞAZALARI AÇ", use_container_width=True, type="primary")
        
    with col_btn2:
        # Bu buton seçim ne olursa olsun hepsini açar
        btn_all = st.button("🌍 TÜM MAĞAZALARI AÇ (HEPSİ)", use_container_width=True)

    # --- Grid Düzeni (Mağaza Seçme Alanı) ---
    st.write("### Mağaza Seçimi")
    st.caption("Açmak istediğin mağazaları işaretle:")
    
    cols = st.columns(5)
    for idx, (name, url) in enumerate(all_links.items()):
        with cols[idx % 5]:
            # Her mağaza için bir checkbox oluşturuyoruz
            # Key parametresi hata almamak için önemli
            is_selected = st.checkbox(name, key=f"check_{idx}")
            if is_selected:
                selected_stores.append(url)

    # --- Açma Mantığı (JavaScript Tetikleyicileri) ---
    
    # 1. Sadece Seçilileri Aç
    if btn_selected:
        if selected_stores:
            js_code = "".join([f"window.open('{link}', '_blank');" for link in selected_stores])
            components.html(f"<script>{js_code}</script>", height=0)
            st.toast(f"{len(selected_stores)} mağaza açılıyor...")
        else:
            st.warning("Önce alttaki listeden mağaza seçmelisin!")

    # 2. Tümünü Aç (Seçimden Bağımsız)
    if btn_all:
        js_code_all = "".join([f"window.open('{link}', '_blank');" for link in all_links.values()])
        components.html(f"<script>{js_code_all}</script>", height=0)
        st.toast("Tüm mağazalar (15 adet) açılıyor...")

    st.write("---")
    st.info("💡 Mağaza isminin yanındaki kutucuğa tıkla, sonra yukarıdaki 'Seçili Mağazaları Aç' butonuna bas.")

else:
    st.info("Plak araması yaparak dükkan listesini gör.")
