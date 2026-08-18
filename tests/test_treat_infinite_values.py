"""Tests für die Behandlung unendlicher Werte."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from application.exceptions import InfiniteValueTreatmentError
from application.flow_dataset import FlowDataset
from application.treat_infinite_values import TreatInfiniteValues


def create_dataset(dataframe: pd.DataFrame) -> FlowDataset:
    """Erzeugt ein FlowDataset und berechnet seine Metadaten."""
    dataset = FlowDataset(
        source=Path("dataset.csv"), dataframe=dataframe, preview=pd.DataFrame(),
        row_count=0, column_count=0, memory_size_bytes=0,
        missing_value_count=0, infinite_value_count=0, label_column="Label",
    )
    dataset.refresh_metadata()
    return dataset


def test_removes_rows_with_positive_and_negative_infinity() -> None:
    dataframe = pd.DataFrame({
        "Rate": [1.0, np.inf, -np.inf, 4.0],
        "Other": [10, 20, 30, 40],
        "Label": ["a", "b", "c", "d"],
    })
    dataset = create_dataset(dataframe)
    original_dataframe = dataset.dataframe

    TreatInfiniteValues().execute(dataset, "Rate", "remove")

    assert dataset.dataframe is original_dataframe
    assert dataset.dataframe["Rate"].tolist() == [1.0, 4.0]
    assert dataset.dataframe["Other"].tolist() == [10, 40]
    assert dataset.row_count == 2
    assert dataset.column_count == 3
    assert dataset.infinite_value_count == 0
    pd.testing.assert_frame_equal(dataset.preview, dataset.dataframe.head(1000))


def test_replaces_positive_and_negative_infinity_with_constant() -> None:
    dataset = create_dataset(pd.DataFrame({
        "Rate": [1.0, np.inf, -np.inf], "Other": [10, 20, 30]
    }))

    TreatInfiniteValues().execute(dataset, "Rate", "replace", "99.5")

    assert dataset.dataframe["Rate"].tolist() == [1.0, 99.5, 99.5]
    assert dataset.dataframe["Other"].tolist() == [10, 20, 30]
    assert dataset.infinite_value_count == 0


@pytest.mark.parametrize("replacement", ["not-a-number", np.nan, np.inf, -np.inf])
def test_rejects_invalid_replacement_without_mutation(replacement: object) -> None:
    dataset = create_dataset(pd.DataFrame({"Rate": [1.0, np.inf]}))
    original = dataset.dataframe.copy(deep=True)

    with pytest.raises(InfiniteValueTreatmentError, match="Ersatzwert"):
        TreatInfiniteValues().execute(dataset, "Rate", "replace", replacement)

    pd.testing.assert_frame_equal(dataset.dataframe, original)
