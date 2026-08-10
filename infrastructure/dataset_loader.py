"""Adapter zum Laden von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


class DatasetLoader:
    """Lädt CSV-Datensätze mit pandas."""

    def load(self, path: Path) -> pd.DataFrame:
        """Lädt eine CSV-Datei und gibt sie als DataFrame zurück."""
        return pd.read_csv(path)
