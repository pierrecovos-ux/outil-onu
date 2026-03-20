import streamlit as st
import requests
from bs4 import BeautifulSoup
import pdfplumber
import re
from rapidfuzz import fuzz

st.set_page_config(page_title="Recherche ONU EN/FR", layout="wide")

st.title("🔎 Recherche bilingue ONU (ultra minimal)")

query = st.text_input("Recherche exacte (avec guillemets)", '"weaponization of religion"')

def search_un(query):
    url = "https://documents.un.org/prod/ods.nsf/home.xsp"
    params = {"q": query}
    r = requests.get(url, params=params)
    soup = BeautifulSoup(r.text, "html.parser")
    
    results = []
    for link in soup.select("a"):
        href = link.get("href")
        if href and "symbol" in href:
            results.append("https://documents.un.org" + href)
        if len(results) >= 5:
            break
    return results

def extract_pdf_text(pdf_url):
    try:
        r = requests.get(pdf_url)
        with open("temp.pdf", "wb") as f:
            f.write(r.content)
        text = ""
        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"
        return text
    except:
        return ""

def highlight(text, query):
    query_clean = query.replace('"', '')
    return re.sub(
        query_clean,
        lambda m: f"**{m.group(0)}**",
        text,
        flags=re.IGNORECASE
    )

def find_occurrences(text, query):
    query_clean = query.replace('"', '')
    sentences = re.split(r'(?<=[.!?])\s+', text)
    matches = []
    for s in sentences:
        if query_clean.lower() in s.lower():
            matches.append(highlight(s, query))
    return matches

def align_fr(en_sentences, fr_text):
    fr_sentences = re.split(r'(?<=[.!?])\s+', fr_text)
    aligned = []
    for en in en_sentences:
        best = ""
        best_score = 0
        for fr in fr_sentences:
            score = fuzz.partial_ratio(en, fr)
            if score > best_score:
                best_score = score
                best = fr
        aligned.append(best)
    return aligned

if st.button("RECHERCHER"):
    results = search_un(query)
    
    for doc in results:
        st.markdown("---")
        st.markdown(f"### 📄 {doc}")

        en_pdf = doc + "&Lang=E"
        fr_pdf = doc + "&Lang=F"

        en_text = extract_pdf_text(en_pdf)
        fr_text = extract_pdf_text(fr_pdf)

        en_matches = find_occurrences(en_text, query)
        fr_matches = align_fr(en_matches, fr_text)

        st.markdown("**EN :**")
        for m in en_matches:
            st.write(m)

        st.markdown("**FR :**")
        for m in fr_matches:
            st.write(m)
