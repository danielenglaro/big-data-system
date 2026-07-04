"""
Modellazione (STUB — Fase 3).

Qui addestreremo e confronteremo i modelli di classificazione con Spark MLlib:
- Logistic Regression
- Decision Tree
- Random Forest
ed eventualmente tuning degli iperparametri con CrossValidator.

Ogni modello e' un Estimator della pipeline MLlib: .fit() sul train produce un
Transformer, che con .transform() genera le predizioni sul test.

Per ora sono solo stub: li implementeremo nella Fase 3.
"""

from pyspark.sql import DataFrame


def train_models(train_df: DataFrame):
    """Addestra e confronta i modelli. TODO: implementare in Fase 3."""
    raise NotImplementedError("train_models() sara' implementata nella Fase 3.")
