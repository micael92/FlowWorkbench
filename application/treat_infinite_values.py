"""Anwendungsfall zum Behandeln unendlicher Werte."""

from __future__ import annotations

import math

import numpy as np
from pandas.api.types import is_numeric_dtype

from application.exceptions import InfiniteValueTreatmentError
from application.flow_dataset import FlowDataset


class TreatInfiniteValues:
    """Entfernt Inf-Zeilen oder ersetzt Inf in einer numerischen Spalte."""

    def execute(
        self,
        dataset: FlowDataset,
        column_name: str,
        operation: str,
        replacement_value: object | None = None,
    ) -> FlowDataset:
        """Validiert die Auswahl und verändert den bestehenden DataFrame."""
        if column_name not in dataset.dataframe.columns:
            raise InfiniteValueTreatmentError(
                f"Die Spalte '{column_name}' ist im Datensatz nicht vorhanden."
            )

        values = dataset.dataframe[column_name]
        if not is_numeric_dtype(values.dtype):
            raise InfiniteValueTreatmentError(
                f"Die Spalte '{column_name}' ist nicht numerisch."
            )

        infinite_rows = np.isinf(values)
        if not infinite_rows.any():
            raise InfiniteValueTreatmentError(
                f"Die Spalte '{column_name}' enthält keine unendlichen Werte."
            )

        if operation not in {"remove", "replace"}:
            raise InfiniteValueTreatmentError("Die gewählte Behandlung ist ungültig.")

        value = replacement_value
        if operation == "replace":
            try:
                value = float(replacement_value)
            except (TypeError, ValueError) as error:
                raise InfiniteValueTreatmentError(
                    "Der Ersatzwert muss numerisch sein."
                ) from error
            if not math.isfinite(value):
                raise InfiniteValueTreatmentError(
                    "Der Ersatzwert muss eine endliche Zahl sein."
                )

        if operation == "remove":
            dataset.dataframe.drop(
                index=dataset.dataframe.index[infinite_rows], inplace=True
            )
        else:
            dataset.dataframe.loc[infinite_rows, column_name] = value

        dataset.refresh_metadata()
        return dataset
