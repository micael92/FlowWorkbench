"""Anwendungsfall zum Berechnen der Labelverteilung."""

import pandas as pd

from application.exceptions import LabelDistributionError
from application.flow_dataset import FlowDataset


class CalculateLabelDistribution:
    """Berechnet absolute und prozentuale Häufigkeiten der Labels."""

    def execute(self, dataset: FlowDataset) -> pd.DataFrame:
        """Berechnet die Verteilung aus der aktuellen Label-Spalte."""
        if dataset.label_column is None:
            raise LabelDistributionError(
                "Für den Datensatz ist keine Label-Spalte festgelegt."
            )

        if dataset.label_column not in dataset.dataframe.columns:
            raise LabelDistributionError(
                f"Die Label-Spalte '{dataset.label_column}' ist im Datensatz "
                "nicht vorhanden."
            )

        if dataset.dataframe.empty:
            raise LabelDistributionError(
                "Der Datensatz enthält keine Zeilen für die Labelverteilung."
            )

        counts = dataset.dataframe[dataset.label_column].value_counts(dropna=False)
        distribution = counts.rename_axis("label").reset_index(name="count")
        distribution["percentage"] = (
            distribution["count"] / len(dataset.dataframe) * 100
        )
        return distribution
