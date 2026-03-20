import streamlit as st
import requests
from bs4 import BeautifulSoup
import urllib.parse

st.set_page_config(page_title="Recherche ONU EN/FR", layout="wide")

st.title("🔎 Recherche bilingue ONU")

query = st.text_input("Recherche exacte (avec guillemets)")

def highlight(text, term):
    return text.replace(term, f"**{term}**")

if st.button("RECHERCHER") and query:

    term = query.replace('"', '')
    encoded = urllib.parse.quote(query)

    # 🔎 Google + filtre ONU
    url = f"https://www.google.com/search?q=site:un.org+{encoded}"

    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.select("div.BNeawe")

    st.markdown("### Résultats")

    count = 0

    for res in results:
        text = res.get_text()

        if term.lower() in text.lower() and len(text) > 40:

            highlighted = highlight(text, term)

            st.markdown(f"🇬🇧 {highlighted}")

            deepl_url = f"https://www.deepl.com/translator#en/fr/{urllib.parse.quote(text)}"
            st.markdown(f"[🔗 Traduire avec DeepL]({deepl_url})")

            st.markdown("---")

            count += 1

        if count >= 5:
            break

    if count == 0:
        st.warning("Aucun résultat trouvé. Essaie sans guillemets ou avec moins de mots.")
