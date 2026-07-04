"""
Sessione Spark centralizzata.

Tutti i moduli del progetto devono ottenere la SparkSession da qui, chiamando
get_spark(). Una sola sessione condivisa garantisce configurazione coerente
(nome app, master, numero di partizioni, livello di log) in tutta la pipeline.
"""

import os
import sys

from pyspark.sql import SparkSession

# Spark avvia dei processi worker Python separati dal driver. Se questi usano
# un interprete diverso (es. il python di sistema) Spark si ferma con
# PYTHON_VERSION_MISMATCH. Forziamo driver e worker a usare lo STESSO interprete
# del processo corrente (quello del venv), impostando le variabili d'ambiente
# che Spark legge per lanciare i worker. sys.executable e' il python in uso ora.
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable


def get_spark() -> SparkSession:
    """
    Crea (o restituisce, se gia' esistente) la SparkSession del progetto.

    SparkSession.builder.getOrCreate() e' idempotente: se una sessione esiste
    gia' nel processo, la riusa invece di crearne una nuova. Cosi' possiamo
    chiamare get_spark() da piu' moduli senza duplicare sessioni.
    """
    spark = (
        SparkSession.builder
        # Nome dell'applicazione: comparira' nella Spark UI e nei log.
        .appName("SpotifyGenreClassification")
        # "local[*]" = esecuzione locale usando tutti i core disponibili della CPU.
        # In un cluster vero qui ci sarebbe l'indirizzo del master (es. yarn).
        .master("local[*]")
        # Numero di partizioni per le operazioni di shuffle (join, groupBy...).
        # Il default e' 200: troppo alto per un dataset piccolo come il nostro,
        # crea overhead. 8 e' un valore ragionevole per l'esecuzione locale.
        .config("spark.sql.shuffle.partitions", "8")
        .getOrCreate()
    )

    # Riduciamo la verbosita' dei log: mostriamo solo warning ed errori,
    # cosi' l'output della pipeline resta leggibile.
    spark.sparkContext.setLogLevel("WARN")

    return spark
