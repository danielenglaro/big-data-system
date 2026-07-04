"""
Interfaccia con MongoDB (via pymongo).

Su MongoDB salviamo SOLO risultati aggregati: metriche dei modelli, confusion
matrix e un campione di predizioni. MAI l'intero dataset (resta su file/Spark).

I dati passano come dizionari Python: pymongo li converte automaticamente in
documenti BSON. Non serve mai creare file .json a mano.
"""

from pymongo import MongoClient

from src.config import MONGO_URI, MONGO_DB


def get_db():
    """
    Apre la connessione e restituisce (client, database).

    Restituiamo anche il client cosi' il chiamante puo' chiuderlo con
    client.close() quando ha finito.
    """
    if not MONGO_URI:
        raise RuntimeError(
            "MONGO_URI non impostata: configura il file .env prima di usare MongoDB."
        )
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return client, db


def salva_risultati(nome_modello: str, metriche: dict, confusion: list) -> None:
    """
    Inserisce un documento nella collection "risultati".

    Parametri
    ---------
    nome_modello : str
        Es. "RandomForest".
    metriche : dict
        Es. {"accuracy": 0.63, "f1": 0.61}.
    confusion : list
        Confusion matrix come lista di liste (JSON/BSON-friendly).
    """
    client, db = get_db()
    try:
        db.risultati.insert_one({
            "modello": nome_modello,
            "metriche": metriche,
            "confusion_matrix": confusion,
        })
        print(f"[db] Risultati di '{nome_modello}' salvati nella collection 'risultati'.")
    finally:
        # Chiudiamo sempre la connessione, anche in caso di errore.
        client.close()


def salva_predizioni(lista_dict: list) -> None:
    """
    Inserisce piu' documenti nella collection "predizioni" con insert_many.

    Parametri
    ---------
    lista_dict : list
        Lista di dizionari, es. output di
        df.select(...).limit(200).toPandas().to_dict(orient="records").
    """
    if not lista_dict:
        print("[db] Nessuna predizione da salvare (lista vuota).")
        return

    client, db = get_db()
    try:
        db.predizioni.insert_many(lista_dict)
        print(f"[db] Salvate {len(lista_dict)} predizioni nella collection 'predizioni'.")
    finally:
        client.close()


def leggi_risultati() -> list:
    """
    Legge tutti i documenti della collection "risultati".

    Escludiamo il campo "_id" (l'ObjectId di Mongo) perche' non e'
    serializzabile facilmente e alla dashboard non serve.

    Ritorna
    -------
    list
        Lista di dizionari (i documenti dei risultati).
    """
    client, db = get_db()
    try:
        # La proiezione {"_id": 0} esclude il campo _id dai documenti restituiti.
        return list(db.risultati.find({}, {"_id": 0}))
    finally:
        client.close()
