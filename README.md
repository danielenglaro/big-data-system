# 🎵 Classificazione del genere musicale con Spark

Progetto universitario di **Big Data**: sistema end-to-end che classifica il
**macro-genere** di una traccia musicale a partire dalle sue audio-features,
usando **Apache Spark (PySpark + MLlib)**, salva i risultati su **MongoDB** e li
mostra in una **dashboard Streamlit**.

Dataset: [`maharshipandya/spotify-tracks-dataset`](https://huggingface.co/datasets/maharshipandya/spotify-tracks-dataset) (~114k tracce) da Hugging Face.

```
Hugging Face → Spark (ingestione → preprocessing → modelli → valutazione) → MongoDB → Streamlit
```

## Struttura
```
src/config.py         # variabili d'ambiente (.env)
src/spark_session.py  # SparkSession centralizzata: get_spark()
src/ingestion.py      # download HF → DataFrame Spark
src/preprocessing.py  # pulizia, macro-generi, feature engineering (stub)
src/modeling.py       # modelli MLlib (stub)
src/evaluation.py     # metriche + confusion matrix (stub)
src/db.py             # interfaccia MongoDB (pymongo)
main.py               # orchestratore della pipeline
dashboard/app.py      # dashboard Streamlit (stub)
```

## 1. Prerequisiti

- **Python 3.10 o 3.11** (PySpark 3.5.1 non supporta ancora 3.12+ in modo affidabile).
- **Java JDK 17** (o 11): Spark gira sulla JVM. Vedi la sezione *JAVA_HOME* sotto.
- **Git**.

## 2. Installazione

```bash
git clone <url-della-repo>
cd big-data-system

# ambiente virtuale (isola le dipendenze del progetto)
python3.11 -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

Verifica veloce che Spark parta:
```bash
python -c "from pyspark.sql import SparkSession; SparkSession.builder.getOrCreate(); print('Spark OK')"
```

## 3. Configurazione del .env

Le credenziali NON stanno nel codice: vanno nel file `.env` (in `.gitignore`).

```bash
cp .env.example .env
```
Poi apri `.env` e inserisci la tua connection string MongoDB:
```
MONGO_URI=mongodb+srv://utente:password@cluster.xxxxx.mongodb.net/
MONGO_DB=spotify_bigdata
```

## 4. Esecuzione

```bash
python main.py
```
Attualmente `main.py` crea la SparkSession, scarica i dati da Hugging Face,
mostra 5 righe e la distribuzione dei generi. Le fasi di preprocessing / modeling
/ evaluation sono segnalate come TODO e verranno collegate qui.

## 5. JAVA_HOME (importante!)

Spark ha bisogno di un JDK. L'errore tipico se manca è `JAVA_HOME is not set`
oppure `Unable to locate a Java Runtime`.

**macOS (con Homebrew):**
```bash
brew install openjdk@17
# collega il JDK al sistema (una volta sola):
sudo ln -sfn /opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk \
     /Library/Java/JavaVirtualMachines/openjdk-17.jdk
# imposta JAVA_HOME (aggiungilo a ~/.zshrc per renderlo permanente):
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

**Windows:** installa Temurin/OpenJDK 17 e imposta `JAVA_HOME` nelle variabili
d'ambiente di sistema, puntando alla cartella del JDK.

Verifica: `java -version` deve stampare la versione 17 (o 11).

## 6. MongoDB

**Opzione consigliata (gruppo): MongoDB Atlas** — cluster M0 gratuito, condiviso.
Copia la connection string `mongodb+srv://...` nel tuo `.env`.

**Alternativa offline: Mongo locale con Docker**
```bash
docker run -d --name mongo -p 27017:27017 mongo:7
```
poi nel `.env`:
```
MONGO_URI=mongodb://localhost:27017/
```

## 7. Dashboard (Fase 5)
```bash
streamlit run dashboard/app.py
```

## Regole del progetto
- Codice commentato **in italiano** (lo spieghiamo all'esame orale).
- Rispettare la struttura in `src/`.
- Non aggiungere dipendenze senza chiedere.
- Mai committare `.env` né il dataset (`data/`).
- Su Mongo solo **risultati aggregati**, mai l'intero dataset.
