import streamlit as st
import pandas as pd
from duckduckgo_search import DDGS

st.set_page_config(page_title="Plak Radar", layout="wide")

st.title("🛡️ Plak Radar: Özgür Mod")
st.write("Google API devreden çıkarıldı. Doğrudan dükkan indeksleri taranıyor...")

query = st.text_input("Aranan Plak/Sanatçı:", placeholder="Örn: Opeth Blackwater Park")

def search_plak(album_name):
    results = []
    # Bakılacak dükkanların listesi
    stores = ["zihni.com", "opus3a.com", "rainbow45records.com", "hammermuzik.com", "rollplak.com"]
    
    with DDGS() as ddgs:
        for store in stores:
            # DuckDuckGo üzerinde 'site:dukkan.com album ismi' araması yapıyoruz
            search_query = f"site:{store} {album_name}"
            try:
                # Sadece ilk sonucu almamız yeterli, en alakalı olan odur
                ddgs_gen = ddgs.text(search_query, region='tr-tr', safesearch='off', timelimit='y')
                for r in ddgs_gen:
                    results.append({
                        "Mağaza": store,
                        "Ürün": r['title'],
                        "Link": r['href'],
                        "Özet": r['body'][:100] + "..." # Fiyat/stok tahmini için
                    })
                    break # Her mağaza için en üstteki sonucu alıp çıkıyoruz
            except Exception as e:
                continue
    return results

if st.button("Dükkanları Tara"):
    if query:
        with st.spinner(f"'{query}' dükkanlarda aranıyor..."):
            data = search_plak(query)
            
            if data:
                df = pd.DataFrame(data)
                
                # Şık bir tablo gösterimi
                st.dataframe(
                    df,
                    use_container_width=True,
                    column_config={
                        "Link": st.column_config.LinkColumn("Satın Al", display_text="Dükkana Git 🛒")
                    }
                )
                st.success(f"{len(data)} mağazada sonuç bulundu!")
            else:
                st.warning("Maalesef hiçbir dükkanda izine rastlayamadık.")
    else:
        st.info("Lütfen bir albüm veya sanatçı ismi yazın.")
