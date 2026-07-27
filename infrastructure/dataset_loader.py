"""Adapter zum Laden von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from domain.exceptions import DatasetLoadError


def load_csv(path: Path) -> pd.DataFrame:
    """Lädt einen CSV-Datensatz in einen DataFrame."""
    try:
        return pd.read_csv(path)
    except (OSError, pd.errors.ParserError) as error:
        raise DatasetLoadError(f"Datensatz konnte nicht geladen werden: {path}") from error
