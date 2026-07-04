"""
Configurazione centralizzata del progetto.

Carica le variabili d'ambiente dal file .env (grazie a python-dotenv) ed espone
MONGO_URI e MONGO_DB al resto del codice. In questo modo le credenziali NON sono
scritte nel codice sorgente: restano nel .env, che e' in .gitignore.
"""

import os
from dotenv import load_dotenv

# load_dotenv() legge il file .env (se presente) e mette le variabili
# dentro os.environ. Se il file non c'e', semplicemente non fa nulla.
load_dotenv()

# Stringa di connessione a MongoDB. Puo' essere None se il .env non e' configurato.
MONGO_URI = os.getenv("MONGO_URI")

# Nome del database; se non specificato usiamo un default sensato.
MONGO_DB = os.getenv("MONGO_DB", "spotify_bigdata")

# Avviso chiaro se manca la configurazione essenziale: cosi' l'utente capisce
# subito cosa fare invece di ricevere un errore criptico piu' avanti.
if not MONGO_URI:
    print(
        "[config] ATTENZIONE: MONGO_URI non impostata.\n"
        "         Copia .env.example in .env e inserisci la tua connection string:\n"
        "             cp .env.example .env\n"
        "         Le funzioni che usano MongoDB non funzioneranno finche' non lo fai."
    )
