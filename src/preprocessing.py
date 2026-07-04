"""
Preprocessing e feature engineering (STUB — Fase 2).

Qui costruiremo la pipeline di preparazione dei dati:
- pulizia e deduplicazione delle tracce;
- mappatura dei ~114 generi in un numero ridotto di MACRO-generi (il target);
- VectorAssembler + StandardScaler sulle audio-features numeriche;
- one-hot encoding su feature categoriche (es. "key", "time_signature");
- StringIndexer sul target;
- split train/test con seme fisso (riproducibilita').

Per ora sono solo stub: li implementeremo nella Fase 2.
"""

from pyspark.sql import DataFrame


def preprocess(df: DataFrame) -> DataFrame:
    """Pulizia + feature engineering. TODO: implementare in Fase 2."""
    raise NotImplementedError("preprocess() sara' implementata nella Fase 2.")
