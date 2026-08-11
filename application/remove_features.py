"""Anwendungsfall zum Entfernen ausgewählter Merkmale."""

from __future__ import annotations

import numpy as np

from application.exceptions import FeatureRemovalError
from application.flow_dataset import FlowDataset


DEFAULT_PREVIEW_ROW_COUNT = 1000


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

        dataset.row_count, dataset.column_count = dataset.dataframe.shape
        dataset.memory_size_bytes = int(
            dataset.dataframe.memory_usage(index=True, deep=True).sum()
        )
        dataset.missing_value_count = int(
            dataset.dataframe.isna().sum().sum()
        )
        numeric_data = dataset.dataframe.select_dtypes(include="number")
        dataset.infinite_value_count = int(np.isinf(numeric_data).sum().sum())
        dataset.preview = dataset.dataframe.head(DEFAULT_PREVIEW_ROW_COUNT)

        return dataset
