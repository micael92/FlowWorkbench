"""Tests für den Datensatz-Loader."""

from pathlib import Path

import pandas as pd

from infrastructure.dataset_loader import DatasetLoader


def test_dataset_loader_reads_dataframe(tmp_path: Path) -> None:
    """Eine CSV-Datei sollte als DataFrame geladen werden."""
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("col_a,col_b\n1,2\n3,4\n", encoding="utf-8")

    result = DatasetLoader().load(csv_path)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["col_a", "col_b"]
    assert result.shape == (2, 2)
