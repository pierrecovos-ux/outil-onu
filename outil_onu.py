import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Recherche ONU EN/FR", layout="wide")

st.title("🔎 Recherche bilingue ONU")

query = st.text_input("Recherche (sans guillemets recommandé)")

def highlight(text, term):
    return text.replace(term, f"**{term}**")

if st.button("RECHERCHER") and query:

    encoded = urllib.parse.quote(query)
    url = f"https://www.bing.com/search?q=site:un.org+{encoded}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.select("li.b_algo")

    found = False

    for r in results:
        text = r.get_text()

        if query.lower() in text.lower():
            st.write("—")
            st.write(highlight(text, query))
            found = True

    if not found:
        st.warning("Aucun résultat trouvé. Essaie avec moins de mots.")
