"""
Valutazione (STUB — Fase 4).

Qui calcoleremo le metriche di classificazione con Spark MLlib:
- accuracy, precision, recall, F1 (con MulticlassClassificationEvaluator);
- confusion matrix.

Attenzione: su un dataset sbilanciato l'accuracy da sola inganna, per questo
guardiamo anche precision/recall/F1 e la confusion matrix.

Per ora sono solo stub: li implementeremo nella Fase 4.
"""

from pyspark.sql import DataFrame


def evaluate(predictions: DataFrame) -> dict:
    """Calcola le metriche sulle predizioni. TODO: implementare in Fase 4."""
    raise NotImplementedError("evaluate() sara' implementata nella Fase 4.")
