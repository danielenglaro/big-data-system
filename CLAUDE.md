# CLAUDE.md — Memoria di progetto

Progetto universitario **Big Data**. Assistente di sviluppo: Claude Code.

## Obiettivo
Classificazione supervisionata del **macro-genere musicale** a partire dalle
audio-features del dataset Hugging Face `maharshipandya/spotify-tracks-dataset`
(~114k tracce). Sistema end-to-end: ingestione → preprocessing → modelli →
valutazione → salvataggio su MongoDB → dashboard.

## Stack
- Python 3.10/3.11 (Spark 3.5.1 non supporta ancora 3.12+ in modo affidabile)
- Apache Spark (PySpark) + Spark MLlib per il calcolo distribuito e i modelli
- MongoDB (via `pymongo`) per i risultati aggregati
- Streamlit per la dashboard
- Spark gira sulla JVM: serve un JDK (17 o 11) e `JAVA_HOME` impostato

## Regole per il codice (IMPORTANTI)
- **Codice commentato in italiano**: dovremo spiegarlo a un esame orale, ogni scelta
  deve essere motivata nei commenti.
- **Rispettare la struttura in `src/`**: ogni responsabilità nel suo modulo
  (config, spark_session, ingestion, preprocessing, modeling, evaluation, db).
- **Non introdurre dipendenze non richieste** senza chiedere prima.
- **Mai committare credenziali né dataset**: `.env` e `data/` sono in `.gitignore`.
- Usare sempre la SparkSession centralizzata in `src/spark_session.py` (`get_spark()`).
- Su MongoDB vanno **solo risultati aggregati** (metriche, confusion matrix, campioni
  di predizioni), MAI l'intero dataset. I dati passano come **dizionari Python**
  (pymongo li salva come BSON), non come file JSON.

## Modello mentale dei dati
```
file (CSV/JSON) → DataFrame Spark → dizionari Python → documenti Mongo (BSON)
   (solo input)     (elaborazione)     (il "ponte")        (storage, automatico)
```
