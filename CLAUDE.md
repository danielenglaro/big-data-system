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

## Ambiente locale (macOS di Daniele) — già configurato e verificato
- **Python**: 3.11.15 installato via Homebrew (`/opt/homebrew/opt/python@3.11`).
  Il sistema ha anche 3.13/3.14, che NON vanno usati con Spark 3.5.1.
- **venv**: `./venv` (creato con il 3.11). Attivare sempre prima di lavorare:
  `source venv/bin/activate`.
- **Java**: OpenJDK 17 via Homebrew. Serve `export JAVA_HOME=/opt/homebrew/opt/openjdk@17`
  (non è permanente finché non lo si aggiunge a `~/.zshrc`).
- **MongoDB**: Atlas (cluster condiviso del gruppo). La `MONGO_URI` sta nel `.env` locale.

### Come eseguire la pipeline
```bash
source venv/bin/activate
export JAVA_HOME=/opt/homebrew/opt/openjdk@17   # se non è in ~/.zshrc
python main.py
```

## Tranelli già risolti (NON reintrodurre)
- **`.gitignore`**: i commenti valgono SOLO a inizio riga. NIENTE commenti inline
  dopo un pattern (`.env  # ...`) → git li tratta come parte del pattern e NON
  ignora il file. È così che stava per essere committato il `.env`.
- **`PYSPARK_PYTHON`**: `src/spark_session.py` imposta `PYSPARK_PYTHON` e
  `PYSPARK_DRIVER_PYTHON` su `sys.executable`. Senza, i worker Spark usano il
  Python di sistema (3.14) e crashano con `PYTHON_VERSION_MISMATCH`. Va sempre
  attivato il venv così driver e worker usano lo stesso interprete.
- **pandas 3.0 / numpy 2.x**: sono stati installati versioni molto recenti; la
  conversione pandas→Spark in `ingestion.py` funziona, ma se emergono attriti
  qui è il primo posto dove guardare.
