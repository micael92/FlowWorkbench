"""Gemeinsames Datenmodell für einen geladenen Flow-Datensatz."""

from dataclasses import dataclass
from pathlib import Path

import pandas as pd


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
