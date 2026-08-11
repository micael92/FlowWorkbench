"""Anwendungsfall zum Berechnen statistischer Kennzahlen."""

from pandas.api.types import is_numeric_dtype

from application.exceptions import StatisticsCalculationError
from application.flow_dataset import FlowDataset
from application.statistic_result import StatisticResult


class CalculateStatistics:
    """Berechnet Kennzahlen für ein numerisches Merkmal eines Datensatzes."""

    def execute(
        self, dataset: FlowDataset, feature_name: str
    ) -> StatisticResult:
        """Berechnet Minimum, Maximum, Mittelwert, Median und Standardabweichung."""
        if feature_name not in dataset.dataframe.columns:
            raise StatisticsCalculationError(
                f"Das Merkmal '{feature_name}' ist im Datensatz nicht vorhanden."
            )

        values = dataset.dataframe[feature_name]
        if not is_numeric_dtype(values.dtype):
            raise StatisticsCalculationError(
                f"Das Merkmal '{feature_name}' ist nicht numerisch auswertbar."
            )

        return StatisticResult(
            feature_name=feature_name,
            minimum=float(values.min()),
            maximum=float(values.max()),
            mean=float(values.mean()),
            median=float(values.median()),
            standard_deviation=float(values.std()),
        )
