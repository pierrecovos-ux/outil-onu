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

    # 🔎 recherche sur site ONU multilingue
    url = f"https://www.un.org/en/search/index.html?query={encoded}"

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")

    results = soup.find_all("a")

    st.markdown("### Résultats")

    count = 0

    for link in results:
        text = link.get_text()

        if term.lower() in text.lower() and len(text) > 30:

            highlighted = highlight(text, term)

            st.markdown(f"🇬🇧 {highlighted}")

            # lien DeepL automatique
            deepl_url = f"https://www.deepl.com/translator#en/fr/{urllib.parse.quote(text)}"
            st.markdown(f"[🔗 Traduire avec DeepL]({deepl_url})")

            st.markdown("---")

            count += 1

        if count >= 5:
            break

    if count == 0:
        st.warning("Aucun résultat trouvé. Essaie sans guillemets.")
