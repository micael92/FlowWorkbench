"""Anwendungsfall zum Importieren eines Datensatzes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from infrastructure.dataset_loader import DatasetLoader


DEFAULT_PREVIEW_ROW_COUNT = 1000


@dataclass
class ImportResult:
    """Enthält den geladenen Datensatz und die wichtigsten Importergebnisse."""

    source: Path
    dataframe: pd.DataFrame
    preview: pd.DataFrame
    row_count: int
    column_count: int
    memory_size_bytes: int
    missing_value_count: int
    infinite_value_count: int


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

    def execute(self, path: Path) -> ImportResult:
        """Importiert einen Datensatz und gibt Daten, Vorschau und Größe zurück."""
        dataframe = self._loader.load(path)
        row_count, column_count = dataframe.shape
        memory_size_bytes = int(dataframe.memory_usage(index=True, deep=True).sum())
        missing_value_count = int(dataframe.isna().sum().sum())
        numeric_data = dataframe.select_dtypes(include="number")
        infinite_value_count = int(np.isinf(numeric_data).sum().sum())

        return ImportResult(
            source=path,
            dataframe=dataframe,
            preview=dataframe.head(self._preview_row_count),
            row_count=row_count,
            column_count=column_count,
            memory_size_bytes=memory_size_bytes,
            missing_value_count=missing_value_count,
            infinite_value_count=infinite_value_count,
        )
