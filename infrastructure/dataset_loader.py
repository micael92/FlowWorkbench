"""Adapter zum Laden von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from domain.exceptions import DatasetLoadError


class DatasetLoader:
    """Lädt CSV-Datensätze mit pandas."""

    def load(self, path: Path) -> pd.DataFrame:
        """Lädt eine CSV-Datei und gibt sie als DataFrame zurück."""
        try:
            return pd.read_csv(path)
        except (OSError, pd.errors.ParserError) as error:
            raise DatasetLoadError(
                f"Datensatz konnte nicht geladen werden: {path}"
            ) from error
