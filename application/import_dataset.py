"""Anwendungsfall zum Importieren eines Datensatzes."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from application.exceptions import DatasetLoadError
from application.flow_dataset import FlowDataset
from infrastructure.dataset_loader import DatasetLoader


DEFAULT_PREVIEW_ROW_COUNT = 1000
KNOWN_LABEL_COLUMN_NAMES = {"label", "labels", "class", "target"}


class ImportDataset:
    """Lädt einen Datensatz und bereitet seine Vorschau und Größe auf."""

    def __init__(
        self,
        loader: DatasetLoader,
        preview_row_count: int = DEFAULT_PREVIEW_ROW_COUNT,
    ) -> None:
        if preview_row_count <= 0:
            raise ValueError("Die Anzahl der Vorschauzeilen muss größer als 0 sein.")

        self._loader = loader
        self._preview_row_count = preview_row_count

    def execute(self, path: Path) -> FlowDataset:
        """Importiert einen Datensatz und gibt Daten, Vorschau und Größe zurück."""
        try:
            dataframe = self._loader.load(path)
        except (OSError, pd.errors.ParserError) as error:
            raise DatasetLoadError(
                f"Datensatz konnte nicht geladen werden: {path}. {error}"
            ) from error

        row_count, column_count = dataframe.shape
        memory_size_bytes = int(dataframe.memory_usage(index=True, deep=True).sum())
        missing_value_count = int(dataframe.isna().sum().sum())
        numeric_data = dataframe.select_dtypes(include="number")
        infinite_value_count = int(np.isinf(numeric_data).sum().sum())
        label_column = self._detect_label_column(dataframe)

        return FlowDataset(
            source=path,
            dataframe=dataframe,
            preview=dataframe.head(self._preview_row_count),
            row_count=row_count,
            column_count=column_count,
            memory_size_bytes=memory_size_bytes,
            missing_value_count=missing_value_count,
            infinite_value_count=infinite_value_count,
            label_column=label_column,
        )

    @staticmethod
    def _detect_label_column(dataframe: pd.DataFrame) -> str | None:
        """Erkennt genau eine bekannte Bezeichnung als Label-Spalte."""
        candidates = [
            column
            for column in dataframe.columns
            if isinstance(column, str)
            and column.lower() in KNOWN_LABEL_COLUMN_NAMES
        ]
        return candidates[0] if len(candidates) == 1 else None
