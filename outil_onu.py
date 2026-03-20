import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.title("🔎 Recherche bilingue ONU (ultra minimal)")

query = st.text_input("Recherche exacte (avec guillemets)")

def highlight(text, term):
    return text.replace(term, f"**{term}**")

if st.button("RECHERCHER") and query:

    encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q=site:un.org+{encoded}"

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.select("div.BNeawe.vvjwJb.AP7Wnd")

    st.markdown("### Résultats")

    for res in results[:5]:
        text = res.get_text()

        if query.replace('"','') in text:
            highlighted = highlight(text, query.replace('"',''))
            st.markdown(highlighted)
