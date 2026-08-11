"""Ergebnis der statistischen Auswertung eines Merkmals."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticResult:
    """Enthält die berechneten Kennzahlen eines numerischen Merkmals."""

    feature_name: str
    minimum: float
    maximum: float
    mean: float
    median: float
    standard_deviation: float
