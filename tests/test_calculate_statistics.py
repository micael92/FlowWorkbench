"""Tests für die Berechnung statistischer Kennzahlen."""

from pathlib import Path

import pandas as pd
import pytest

from application.calculate_statistics import CalculateStatistics
from application.exceptions import StatisticsCalculationError
from application.flow_dataset import FlowDataset
from application.statistic_result import StatisticResult


def create_dataset(dataframe: pd.DataFrame) -> FlowDataset:
    """Erzeugt einen kleinen FlowDataset für die Tests des Use Cases."""
    return FlowDataset(
        source=Path("dataset.csv"),
        dataframe=dataframe,
        preview=dataframe.head(1000),
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        memory_size_bytes=0,
        missing_value_count=0,
        infinite_value_count=0,
    )


def test_calculate_statistics_returns_all_values_for_numeric_feature() -> None:
    dataset = create_dataset(pd.DataFrame({"packets": [1.0, 2.0, 3.0, 4.0]}))

    result = CalculateStatistics().execute(dataset, "packets")

    assert isinstance(result, StatisticResult)
    assert result.feature_name == "packets"
    assert result.minimum == 1.0
    assert result.maximum == 4.0
    assert result.mean == 2.5
    assert result.median == 2.5
    assert result.standard_deviation == pytest.approx(1.2909944487)


def test_calculate_statistics_rejects_non_numeric_feature() -> None:
    dataset = create_dataset(pd.DataFrame({"protocol": ["TCP", "UDP"]}))

    with pytest.raises(StatisticsCalculationError, match="nicht numerisch"):
        CalculateStatistics().execute(dataset, "protocol")


def test_calculate_statistics_uses_pandas_nan_behavior() -> None:
    dataset = create_dataset(pd.DataFrame({"duration": [1.0, None, 3.0]}))

    result = CalculateStatistics().execute(dataset, "duration")

    assert result.minimum == 1.0
    assert result.maximum == 3.0
    assert result.mean == 2.0
    assert result.median == 2.0
    assert result.standard_deviation == pytest.approx(2**0.5)
