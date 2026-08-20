"""Tests für den Datensatz-Loader."""

from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from infrastructure.dataset_loader import MAX_CSV_FILE_SIZE_BYTES, DatasetLoader


def test_dataset_loader_reads_dataframe(tmp_path: Path) -> None:
    """Eine CSV-Datei sollte als DataFrame geladen werden."""
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("col_a,col_b\n1,2\n3,4\n", encoding="utf-8")

    result = DatasetLoader().load(csv_path)

    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["col_a", "col_b"]
    assert result.shape == (2, 2)


@pytest.mark.parametrize(
    "file_size", [MAX_CSV_FILE_SIZE_BYTES - 1, MAX_CSV_FILE_SIZE_BYTES]
)
def test_dataset_loader_accepts_file_at_or_below_size_limit(
    monkeypatch: pytest.MonkeyPatch, file_size: int
) -> None:
    expected = pd.DataFrame({"value": [1]})
    read_paths: list[Path] = []
    path = Path("dataset.csv")
    monkeypatch.setattr(
        Path, "stat", lambda self: SimpleNamespace(st_size=file_size)
    )
    monkeypatch.setattr(
        pd,
        "read_csv",
        lambda read_path: read_paths.append(read_path) or expected,
    )

    result = DatasetLoader().load(path)

    assert result is expected
    assert read_paths == [path]


def test_dataset_loader_rejects_oversized_file_before_read_csv(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    path = Path("dataset.csv")
    monkeypatch.setattr(
        Path,
        "stat",
        lambda self: SimpleNamespace(st_size=MAX_CSV_FILE_SIZE_BYTES + 1),
    )

    def fail_if_called(path: Path) -> pd.DataFrame:
        pytest.fail(f"pd.read_csv() wurde unerwartet aufgerufen: {path}")

    monkeypatch.setattr(pd, "read_csv", fail_if_called)

    with pytest.raises(OSError, match=r"zu groß.*500 MiB"):
        DatasetLoader().load(path)
