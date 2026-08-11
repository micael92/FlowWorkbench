"""Tests für das Entfernen ausgewählter Merkmale."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from application.exceptions import FeatureRemovalError
from application.flow_dataset import FlowDataset
from application.remove_features import RemoveFeatures


def create_dataset(dataframe: pd.DataFrame) -> FlowDataset:
    """Erzeugt ein FlowDataset mit Metadaten für die Tests."""
    numeric_data = dataframe.select_dtypes(include="number")
    return FlowDataset(
        source=Path("dataset.csv"),
        dataframe=dataframe,
        preview=dataframe.head(1000),
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        memory_size_bytes=int(dataframe.memory_usage(index=True, deep=True).sum()),
        missing_value_count=int(dataframe.isna().sum().sum()),
        infinite_value_count=int(np.isinf(numeric_data).sum().sum()),
        label_column="Label",
    )


def test_remove_single_feature_and_keep_other_features_and_label() -> None:
    dataset = create_dataset(
        pd.DataFrame(
            {
                "Flow ID": ["a", "b"],
                "Duration": [1, 2],
                "Label": ["normal", "attack"],
            }
        )
    )

    result = RemoveFeatures().execute(dataset, ["Flow ID"])

    assert result is dataset
    assert list(dataset.dataframe.columns) == ["Duration", "Label"]
    assert "Label" in dataset.dataframe.columns


def test_remove_multiple_features_in_one_call() -> None:
    dataset = create_dataset(
        pd.DataFrame(
            {
                "Flow ID": ["a"],
                "Src IP": ["10.0.0.1"],
                "Duration": [1],
                "Label": ["normal"],
            }
        )
    )

    RemoveFeatures().execute(dataset, ["Flow ID", "Src IP"])

    assert list(dataset.dataframe.columns) == ["Duration", "Label"]


def test_remove_rejects_label_column_without_changing_dataframe() -> None:
    dataset = create_dataset(pd.DataFrame({"Duration": [1], "Label": ["normal"]}))
    original_dataframe = dataset.dataframe.copy()

    with pytest.raises(FeatureRemovalError, match="Label-Spalte"):
        RemoveFeatures().execute(dataset, ["Label"])

    pd.testing.assert_frame_equal(dataset.dataframe, original_dataframe)


def test_remove_rejects_unknown_feature_without_changing_dataframe() -> None:
    dataset = create_dataset(pd.DataFrame({"Duration": [1], "Label": ["normal"]}))
    original_dataframe = dataset.dataframe.copy()

    with pytest.raises(FeatureRemovalError, match="Unknown"):
        RemoveFeatures().execute(dataset, ["Unknown"])

    pd.testing.assert_frame_equal(dataset.dataframe, original_dataframe)


def test_remove_updates_counts_preview_and_dataframe_in_place() -> None:
    dataframe = pd.DataFrame(
        {
            "Remove": [1, 2, 3],
            "Keep": [4, 5, 6],
            "Label": ["a", "b", "c"],
        }
    )
    dataset = create_dataset(dataframe)
    original_dataframe = dataset.dataframe

    RemoveFeatures().execute(dataset, ["Remove"])

    assert dataset.dataframe is original_dataframe
    assert dataset.row_count == 3
    assert dataset.column_count == 2
    assert list(dataset.preview.columns) == ["Keep", "Label"]
    pd.testing.assert_frame_equal(dataset.preview, dataset.dataframe.head(1000))


def test_remove_recalculates_memory_missing_and_infinite_value_counts() -> None:
    dataframe = pd.DataFrame(
        {
            "Remove": [np.nan, np.inf],
            "Keep": [1.0, np.nan],
            "Label": ["normal", "attack"],
        }
    )
    dataset = create_dataset(dataframe)
    previous_memory_size = dataset.memory_size_bytes

    RemoveFeatures().execute(dataset, ["Remove"])

    expected_memory_size = int(
        dataset.dataframe.memory_usage(index=True, deep=True).sum()
    )
    assert dataset.memory_size_bytes == expected_memory_size
    assert dataset.memory_size_bytes < previous_memory_size
    assert dataset.missing_value_count == 1
    assert dataset.infinite_value_count == 0


def test_remove_with_empty_selection_keeps_dataset_unchanged() -> None:
    dataset = create_dataset(pd.DataFrame({"Duration": [1], "Label": ["normal"]}))
    original_dataframe = dataset.dataframe

    result = RemoveFeatures().execute(dataset, [])

    assert result is dataset
    assert dataset.dataframe is original_dataframe
    assert list(dataset.dataframe.columns) == ["Duration", "Label"]
