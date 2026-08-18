"""Tests für die Behandlung fehlender Werte."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from application.exceptions import MissingValueTreatmentError
from application.flow_dataset import FlowDataset
from application.treat_missing_values import TreatMissingValues


def create_dataset(dataframe: pd.DataFrame) -> FlowDataset:
    """Erzeugt ein FlowDataset und berechnet seine Metadaten."""
    dataset = FlowDataset(
        source=Path("dataset.csv"), dataframe=dataframe, preview=pd.DataFrame(),
        row_count=0, column_count=0, memory_size_bytes=0,
        missing_value_count=0, infinite_value_count=0, label_column="Label",
    )
    dataset.refresh_metadata()
    return dataset


def test_removes_rows_with_nan_and_refreshes_dataset() -> None:
    dataframe = pd.DataFrame({
        "Duration": [1.0, np.nan, 3.0],
        "Other": [np.nan, 20.0, 30.0],
        "Label": ["a", "b", "c"],
    })
    dataset = create_dataset(dataframe)
    original_dataframe = dataset.dataframe

    result = TreatMissingValues().execute(dataset, "Duration", "remove")

    assert result is dataset
    assert dataset.dataframe is original_dataframe
    assert dataset.dataframe["Duration"].tolist() == [1.0, 3.0]
    assert dataset.dataframe["Other"].isna().sum() == 1
    assert dataset.row_count == 2
    assert dataset.column_count == 3
    assert dataset.missing_value_count == 1
    pd.testing.assert_frame_equal(dataset.preview, dataset.dataframe.head(1000))


def test_replaces_nan_with_constant_and_keeps_other_values() -> None:
    dataset = create_dataset(pd.DataFrame({
        "Duration": [1.0, np.nan, 3.0],
        "Other": [10, 20, 30],
        "Label": ["a", "b", "c"],
    }))

    TreatMissingValues().execute(dataset, "Duration", "replace", "0")

    assert dataset.dataframe["Duration"].tolist() == [1.0, 0.0, 3.0]
    assert dataset.dataframe["Other"].tolist() == [10, 20, 30]
    assert dataset.missing_value_count == 0
    assert dataset.infinite_value_count == 0


def test_unknown_column_is_rejected_without_mutation() -> None:
    dataset = create_dataset(pd.DataFrame({"Duration": [1.0, np.nan]}))
    original = dataset.dataframe.copy(deep=True)

    with pytest.raises(MissingValueTreatmentError, match="nicht vorhanden"):
        TreatMissingValues().execute(dataset, "Unknown", "remove")

    pd.testing.assert_frame_equal(dataset.dataframe, original)
