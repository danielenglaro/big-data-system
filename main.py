"""
Orchestratore della pipeline.

Per ora esegue le fasi gia' pronte:
1. crea la SparkSession centralizzata;
2. carica i dati da Hugging Face;
3. mostra un campione e la distribuzione dei generi.

Le fasi di preprocessing / modeling / evaluation sono lasciate come TODO:
le collegheremo qui man mano che le implementiamo.

Esecuzione:
    python main.py
"""

from pyspark.sql import functions as F

from src.spark_session import get_spark
from src.ingestion import load_data


def main():
    # 1) Sessione Spark condivisa da tutta la pipeline.
    spark = get_spark()
    print("[main] SparkSession avviata.")

    # 2) Ingestione dei dati (Hugging Face -> DataFrame Spark).
    df = load_data(spark)

    # 3) Anteprima delle prime 5 righe.
    print("[main] Anteprima delle prime 5 righe:")
    df.show(5)

    # 4) Distribuzione dei generi: quante tracce per ciascun 'track_genre',
    #    ordinate dalla piu' frequente. Utile per capire lo sbilanciamento
    #    delle classi prima di costruire i macro-generi.
    print("[main] Distribuzione dei generi (track_genre):")
    (
        df.groupBy("track_genre")
        .count()
        .orderBy(F.desc("count"))
        .show(truncate=False)
    )

    # --- TODO prossime fasi ---
    # from src.preprocessing import preprocess
    # from src.modeling import train_models
    # from src.evaluation import evaluate
    #
    # df_prep = preprocess(df)                 # Fase 2: pulizia + feature engineering
    # train_df, test_df = df_prep.randomSplit([0.8, 0.2], seed=42)
    # modello, predictions = train_models(train_df)  # Fase 3: training
    # metriche = evaluate(predictions)         # Fase 4: metriche + confusion matrix
    # from src.db import salva_risultati
    # salva_risultati("RandomForest", metriche["scores"], metriche["confusion"])

    # Chiudiamo la sessione al termine.
    spark.stop()
    print("[main] Pipeline terminata.")


if __name__ == "__main__":
    main()
