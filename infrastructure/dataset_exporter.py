"""Adapter zum Exportieren von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def export_csv(dataframe: pd.DataFrame, path: Path) -> None:
    """Exportiert einen DataFrame als CSV-Datei."""
    dataframe.to_csv(path, index=False)
