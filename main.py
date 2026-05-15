import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

st.set_page_config(page_title="Plak Radar", page_icon=" vinyl")

st.title("🛡️ Plak Radar")
st.subheader("Mağaza Mağaza Gezmeye Son!")

query = st.text_input("Aranacak Plak / Sanatçı:", placeholder="Örn: Camel - Moonmadness")

def search_opus3a(plak_adi):
    url = f"https://www.opus3a.com/arama?q={plak_adi}"
    # Buraya sitenin içinden veri çekme (scraping) kodları gelecek
    return {"Mağaza": "Opus3a", "Durum": "Kontrol Et", "Link": url}

def search_hammer(plak_adi):
    url = f"https://hammermuzik.com/?s={plak_adi}&post_type=product"
    return {"Mağaza": "Hammer Müzik", "Durum": "Kontrol Et", "Link": url}

def search_rollplak(plak_adi):
    url = f"https://www.rollplak.com/arama?q={plak_adi}"
    return {"Mağaza": "Rollplak", "Durum": "Kontrol Et", "Link": url}

if st.button("Tüm Mağazalarda Ara"):
    if query:
        with st.spinner("Plak dükkanlarına bakılıyor..."):
            # Tüm siteleri listeliyoruz
            results = [
                search_opus3a(query),
                search_hammer(query),
                search_rollplak(query)
            ]
            
            df = pd.DataFrame(results)
            # Linkleri tıklanabilir yapıyoruz
            st.dataframe(df, column_config={
                "Link": st.column_config.LinkColumn("Mağazaya Git")
            })
    else:
        st.warning("Lütfen bir isim girin.")
