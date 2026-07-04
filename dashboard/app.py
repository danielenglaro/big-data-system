"""
Dashboard Streamlit (STUB — Fase 5).

Leggera' i risultati da MongoDB (via src.db.leggi_risultati) e mostrera':
- tabella di confronto dei modelli;
- confusion matrix come heatmap (seaborn);
- distribuzione dei macro-generi.

Avvio (una volta implementata):
    streamlit run dashboard/app.py

Per ora e' un semplice segnaposto che verifica solo che Streamlit parta.
"""

import streamlit as st

st.title("🎵 Classificazione del genere musicale — Dashboard")
st.info("Dashboard in costruzione (Fase 5). Qui mostreremo metriche e confusion matrix.")

# TODO Fase 5: leggere i risultati da Mongo e visualizzarli.
#   from src.db import leggi_risultati
#   risultati = leggi_risultati()
#   st.dataframe(risultati)
