"""
Ingestione dei dati.

Scarica il dataset delle tracce Spotify da Hugging Face e lo trasforma in un
DataFrame Spark, che e' la struttura dati su cui lavora tutta la pipeline.

Flusso: Hugging Face (tabella) -> pandas -> DataFrame Spark.
Il dataset e' piccolo (~114k righe), quindi il passaggio via pandas sul driver
e' accettabile. Su volumi enormi si leggerebbe direttamente in formato distribuito.
"""

from pyspark.sql import DataFrame, SparkSession

# Identificativo del dataset su Hugging Face Hub.
HF_DATASET = "maharshipandya/spotify-tracks-dataset"

# Percorso del CSV locale usato dal fallback (vedi sotto).
CSV_LOCALE = "data/spotify.csv"


def load_data(spark: SparkSession) -> DataFrame:
    """
    Carica le tracce e restituisce un DataFrame Spark.

    Strategia principale: scarica lo split "train" da Hugging Face, lo converte
    in pandas e poi in DataFrame Spark.

    Parametri
    ---------
    spark : SparkSession
        La sessione ottenuta da src.spark_session.get_spark().

    Ritorna
    -------
    DataFrame
        Il DataFrame Spark con le tracce.
    """
    # datasets e' importato qui dentro (non in cima) cosi' il modulo si puo'
    # importare anche in ambienti dove la libreria non serve subito.
    from datasets import load_dataset

    print(f"[ingestion] Scarico '{HF_DATASET}' (split train) da Hugging Face...")
    ds = load_dataset(HF_DATASET, split="train")

    # to_pandas() materializza la tabella in un DataFrame pandas sul driver.
    pdf = ds.to_pandas()
    print(f"[ingestion] Ricevute {len(pdf)} righe da Hugging Face.")

    # Il dataset HF include spesso una colonna indice senza nome ("Unnamed: 0"):
    # la rimuoviamo se presente, non ci serve.
    if "Unnamed: 0" in pdf.columns:
        pdf = pdf.drop(columns=["Unnamed: 0"])

    # createDataFrame converte il pandas DataFrame in un DataFrame Spark distribuito.
    df = spark.createDataFrame(pdf)

    # --- FALLBACK: lettura da CSV locale ---
    # Se non si ha accesso a internet, o si vuole lavorare offline, si puo'
    # scaricare una volta il CSV in data/spotify.csv e usare questa riga al posto
    # del blocco Hugging Face qui sopra:
    #
    #   df = spark.read.csv(CSV_LOCALE, header=True, inferSchema=True)
    #
    # Il resto della pipeline non cambia: da qui in poi lavoriamo su un DataFrame Spark.

    # Stampiamo count e schema come verifica che l'ingestione sia andata a buon fine.
    print(f"[ingestion] DataFrame Spark creato: {df.count()} righe.")
    print("[ingestion] Schema del DataFrame:")
    df.printSchema()

    return df
