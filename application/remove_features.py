"""Anwendungsfall zum Entfernen ausgewählter Merkmale."""

from __future__ import annotations

from application.exceptions import FeatureRemovalError
from application.flow_dataset import FlowDataset


class RemoveFeatures:
    """Entfernt ausgewählte Spalten und aktualisiert den Datensatz."""

    def execute(
        self, dataset: FlowDataset, feature_names: list[str]
    ) -> FlowDataset:
        """Validiert und entfernt Merkmale aus dem bestehenden DataFrame."""
        if not feature_names:
            return dataset

        if dataset.label_column in feature_names:
            raise FeatureRemovalError("Die Label-Spalte darf nicht entfernt werden.")

        missing_features = [
            feature_name
            for feature_name in feature_names
            if feature_name not in dataset.dataframe.columns
        ]
        if missing_features:
            names = ", ".join(str(name) for name in missing_features)
            raise FeatureRemovalError(
                f"Folgende Merkmale sind im Datensatz nicht vorhanden: {names}"
            )

        dataset.dataframe.drop(columns=feature_names, inplace=True)
        dataset.refresh_metadata()

        return dataset
