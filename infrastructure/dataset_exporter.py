"""Adapter zum Exportieren von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from domain.exceptions import DatasetExportError


def export_csv(dataframe: pd.DataFrame, path: Path) -> None:
    """Exportiert einen DataFrame als CSV-Datei."""
    try:
        dataframe.to_csv(path, index=False)
    except OSError as error:
        raise DatasetExportError(
            f"Datensatz konnte nicht exportiert werden: {path}"
        ) from error
