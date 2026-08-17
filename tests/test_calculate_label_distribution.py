"""Tests für die Berechnung der Labelverteilung."""

from pathlib import Path

import pandas as pd
import pytest

from application.calculate_label_distribution import CalculateLabelDistribution
from application.exceptions import LabelDistributionError
from application.flow_dataset import FlowDataset


def create_dataset(
    dataframe: pd.DataFrame, label_column: str | None = "Label"
) -> FlowDataset:
    """Erzeugt einen kleinen FlowDataset für die Tests des Use Cases."""
    return FlowDataset(
        source=Path("dataset.csv"),
        dataframe=dataframe,
        preview=dataframe.head(1000),
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        memory_size_bytes=0,
        missing_value_count=int(dataframe.isna().sum().sum()),
        infinite_value_count=0,
        label_column=label_column,
    )


def test_calculates_counts_and_percentages_for_multiple_labels() -> None:
    dataset = create_dataset(
        pd.DataFrame({"Label": ["BENIGN", "Attack", "BENIGN", "BENIGN"]})
    )

    result = CalculateLabelDistribution().execute(dataset)

    assert list(result.columns) == ["label", "count", "percentage"]
    assert result.to_dict("records") == [
        {"label": "BENIGN", "count": 3, "percentage": 75.0},
        {"label": "Attack", "count": 1, "percentage": 25.0},
    ]


def test_counts_missing_label_values_as_a_separate_value() -> None:
    dataset = create_dataset(
        pd.DataFrame({"Label": ["BENIGN", None, "BENIGN", None]})
    )

    result = CalculateLabelDistribution().execute(dataset)

    assert result["count"].sum() == len(dataset.dataframe)
    missing_row = result[result["label"].isna()].iloc[0]
    assert missing_row["count"] == 2
    assert missing_row["percentage"] == 50.0


def test_distribution_totals_match_the_current_number_of_rows() -> None:
    dataset = create_dataset(
        pd.DataFrame(
            {"Label": ["BENIGN", "Attack", "BENIGN", "PortScan", "BENIGN"]}
        )
    )

    result = CalculateLabelDistribution().execute(dataset)

    assert result["count"].sum() == len(dataset.dataframe)
    assert result["percentage"].sum() == pytest.approx(100.0)


def test_rejects_dataset_without_selected_label_column() -> None:
    dataset = create_dataset(pd.DataFrame({"Category": ["BENIGN"]}), None)

    with pytest.raises(LabelDistributionError, match="keine Label-Spalte"):
        CalculateLabelDistribution().execute(dataset)


def test_rejects_label_column_missing_from_current_dataframe() -> None:
    dataset = create_dataset(pd.DataFrame({"Duration": [1, 2]}))

    with pytest.raises(LabelDistributionError, match="nicht vorhanden"):
        CalculateLabelDistribution().execute(dataset)


def test_uses_current_dataframe_after_it_has_changed() -> None:
    dataframe = pd.DataFrame(
        {"Duration": [1, 2, 3], "Label": ["BENIGN", "Attack", "Attack"]}
    )
    dataset = create_dataset(dataframe)
    dataset.dataframe.drop(index=2, inplace=True)

    result = CalculateLabelDistribution().execute(dataset)

    assert result["count"].sum() == 2
    assert result.set_index("label")["percentage"].to_dict() == {
        "BENIGN": 50.0,
        "Attack": 50.0,
    }


def test_rejects_empty_dataframe() -> None:
    dataset = create_dataset(pd.DataFrame({"Label": []}))

    with pytest.raises(LabelDistributionError, match="keine Zeilen"):
        CalculateLabelDistribution().execute(dataset)
