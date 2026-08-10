"""Unit-Tests für den Anwendungsfall zum Importieren eines Datensatzes."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from application.import_dataset import ImportDataset
from domain.exceptions import DatasetLoadError
from infrastructure.dataset_loader import DatasetLoader


class RecordingLoader(DatasetLoader):
    """Gibt Testdaten zurück und merkt sich den verwendeten Pfad."""

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe
        self.loaded_path: Path | None = None

    def load(self, path: Path) -> pd.DataFrame:
        """Zeichnet den Pfad auf und gibt das vorbereitete DataFrame zurück."""
        self.loaded_path = path
        return self.dataframe


def test_import_uses_loader_and_returns_dataset_information() -> None:
    path = Path("dataset.csv")
    dataframe = pd.DataFrame(
        {"source": ["A", "C", "E"], "destination": ["B", "D", "F"]}
    )
    loader = RecordingLoader(dataframe)

    result = ImportDataset(loader).execute(path)

    assert loader.loaded_path == path
    assert result.source == path
    assert result.dataframe is dataframe
    assert result.row_count == 3
    assert result.column_count == 2
    assert result.missing_value_count == 0
    assert result.infinite_value_count == 0


def test_import_counts_missing_and_infinite_values_in_mixed_data() -> None:
    dataframe = pd.DataFrame(
        {
            "number": [1.0, np.inf, -np.inf, np.nan],
            "other_number": [np.nan, 2.0, 3.0, 4.0],
            "text": ["normal", "inf", None, "-inf"],
            "category": pd.Series(["A", "B", "A", None], dtype="category"),
        }
    )

    result = ImportDataset(RecordingLoader(dataframe)).execute(Path("dataset.csv"))

    assert result.row_count == 4
    assert result.column_count == 4
    assert result.missing_value_count == 4
    assert result.infinite_value_count == 2


def test_import_returns_positive_python_int_memory_size() -> None:
    dataframe = pd.DataFrame({"text": ["a longer text value", "another value"]})

    result = ImportDataset(RecordingLoader(dataframe)).execute(Path("dataset.csv"))

    assert type(result.memory_size_bytes) is int
    assert result.memory_size_bytes > 0
    assert result.memory_size_bytes == int(
        dataframe.memory_usage(index=True, deep=True).sum()
    )


def test_import_limits_preview_to_configured_number_of_rows() -> None:
    dataframe = pd.DataFrame({"number": range(5)})

    result = ImportDataset(RecordingLoader(dataframe), preview_row_count=2).execute(
        Path("dataset.csv")
    )

    pd.testing.assert_frame_equal(result.preview, dataframe.head(2))


def test_import_limits_default_preview_to_1000_rows() -> None:
    dataframe = pd.DataFrame({"number": range(1001)})

    result = ImportDataset(RecordingLoader(dataframe)).execute(Path("dataset.csv"))

    pd.testing.assert_frame_equal(result.preview, dataframe.head(1000))


def test_import_uses_all_rows_below_preview_limit() -> None:
    dataframe = pd.DataFrame({"number": range(999)})

    result = ImportDataset(RecordingLoader(dataframe)).execute(Path("dataset.csv"))

    pd.testing.assert_frame_equal(result.preview, dataframe)


@pytest.mark.parametrize("preview_row_count", [0, -1])
def test_import_rejects_invalid_preview_size(preview_row_count: int) -> None:
    loader = RecordingLoader(pd.DataFrame())

    with pytest.raises(ValueError, match="größer als 0"):
        ImportDataset(loader, preview_row_count=preview_row_count)


def test_import_propagates_dataset_load_error(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.csv"

    with pytest.raises(DatasetLoadError):
        ImportDataset(DatasetLoader()).execute(missing_path)
