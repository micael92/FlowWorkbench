"""Adapter zum Laden von Datensätzen."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


MAX_CSV_FILE_SIZE_BYTES = 500 * 1024 * 1024


class DatasetLoader:
    """Lädt CSV-Datensätze mit pandas."""

    def load(self, path: Path) -> pd.DataFrame:
        """Lädt eine CSV-Datei und gibt sie als DataFrame zurück."""
        if path.stat().st_size > MAX_CSV_FILE_SIZE_BYTES:
            raise OSError(
                "Die CSV-Datei ist zu groß. Die maximale Größe beträgt 500 MiB."
            )

        return pd.read_csv(path)
