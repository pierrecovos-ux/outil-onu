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

    term = query
    encoded = urllib.parse.quote(query)

    # 🔎 DuckDuckGo (version HTML = non bloquée)
    url = f"https://html.duckduckgo.com/html/?q=site:un.org+{encoded}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.find_all("a", class_="result__a")

    st.markdown("### Résultats")

    count = 0

    for res in results:
        text = res.get_text()

        if term.lower() in text.lower():

            highlighted = highlight(text, term)

            st.markdown(f"🇬🇧 {highlighted}")

            deepl_url = f"https://www.deepl.com/translator#en/fr/{urllib.parse.quote(text)}"
            st.markdown(f"[🔗 Traduire avec DeepL]({deepl_url})")

            st.markdown("---")

            count += 1

        if count >= 5:
            break

    if count == 0:
        st.warning("Aucun résultat trouvé. Essaie avec moins de mots.")
