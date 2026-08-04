"""Anwendungsfall zum Importieren eines Datensatzes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from infrastructure.dataset_loader import DatasetLoader


DEFAULT_PREVIEW_ROW_COUNT = 100


@dataclass
class ImportDatasetResult:
    """Enthält den geladenen Datensatz und die wichtigsten Importergebnisse."""

    source: Path
    dataframe: pd.DataFrame
    preview: pd.DataFrame
    row_count: int
    column_count: int


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

    def execute(self, path: Path) -> ImportDatasetResult:
        """Importiert einen Datensatz und gibt Daten, Vorschau und Größe zurück."""
        dataframe = self._loader.load(path)
        row_count, column_count = dataframe.shape

        return ImportDatasetResult(
            source=path,
            dataframe=dataframe,
            preview=dataframe.head(self._preview_row_count),
            row_count=row_count,
            column_count=column_count,
        )
