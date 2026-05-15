import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Plak Radar Pro", page_icon=" vinyl", layout="wide")

st.title("🛡️ Plak Radar: Opeth Modu")
st.write("Dükkanların içinde arama yapmak yerine, doğrudan dükkan bazlı arama motorunu kullanıyoruz.")

query = st.text_input("Aradığınız Albüm / Sanatçı:", placeholder="Örn: Opeth Damnation")

# Mağaza listesi ve arama şablonları
def generate_links(search_query):
    encoded_query = urllib.parse.quote(search_query)
    
    # Mağazaların kendi iç arama link yapıları
    stores = [
        {"Mağaza": "Zihni Müzik", "Link": f"https://www.zihni.com/arama/{encoded_query}"},
        {"Mağaza": "Opus3a", "Link": f"https://www.opus3a.com/ara?q={encoded_query}"},
        {"Mağaza": "Rainbow45", "Link": f"https://www.rainbow45records.com/arama?q={encoded_query}"},
        {"Mağaza": "Hammer Müzik", "Link": f"https://hammermuzik.com/?s={encoded_query}&post_type=product"},
        {"Mağaza": "Rollplak", "Link": f"https://www.rollplak.com/arama?q={encoded_query}"},
        {"Mağaza": "Plaksepeti", "Link": f"https://www.plaksepeti.com/arama?q={encoded_query}"}
    ]
    return stores

if query:
    st.subheader(f"🔍 '{query}' için Sonuç Paneli")
    
    results = generate_links(query)
    
    # Şık bir tablo ve butonlar oluşturalım
    cols = st.columns(3) # Sonuçları 3 sütuna bölelim
    
    for i, res in enumerate(results):
        with cols[i % 3]:
            st.info(f"**{res['Mağaza']}**")
            # Her mağaza için doğrudan arama sayfasına giden bir buton
            st.link_button(f"{res['Mağaza']}'da Sonuçları Gör", res['Link'], use_container_width=True)

    st.divider()
    st.caption("Not: Mağazaların güvenlik duvarları anlık veri çekmeyi engellediği için, en güncel stok ve fiyat bilgisini yukarıdaki butonlara basarak doğrudan mağaza sayfasında görebilirsin.")
else:
    st.warning("Lütfen bir plak adı girerek radarı başlatın.")
