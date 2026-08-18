"""Gemeinsames Datenmodell für einen geladenen Flow-Datensatz."""

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


DEFAULT_PREVIEW_ROW_COUNT = 1000


@dataclass
class FlowDataset:
    """Enthält den geladenen Datensatz und seine wichtigsten Eigenschaften."""

    source: Path
    dataframe: pd.DataFrame
    preview: pd.DataFrame
    row_count: int
    column_count: int
    memory_size_bytes: int
    missing_value_count: int
    infinite_value_count: int
    label_column: str | None

    def refresh_metadata(self) -> None:
        """Berechnet Vorschau und abgeleitete Angaben aus dem DataFrame neu."""
        self.row_count, self.column_count = self.dataframe.shape
        self.memory_size_bytes = int(
            self.dataframe.memory_usage(index=True, deep=True).sum()
        )
        self.missing_value_count = int(self.dataframe.isna().sum().sum())
        numeric_data = self.dataframe.select_dtypes(include="number")
        self.infinite_value_count = int(np.isinf(numeric_data).sum().sum())
        self.preview = self.dataframe.head(DEFAULT_PREVIEW_ROW_COUNT)
