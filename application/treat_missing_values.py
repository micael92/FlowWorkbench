"""Anwendungsfall zum Behandeln fehlender Werte."""

from __future__ import annotations

from pandas.api.types import is_numeric_dtype

from application.exceptions import MissingValueTreatmentError
from application.flow_dataset import FlowDataset


class TreatMissingValues:
    """Entfernt NaN-Zeilen oder ersetzt NaN in einer ausgewählten Spalte."""

    def execute(
        self,
        dataset: FlowDataset,
        column_name: str,
        operation: str,
        replacement_value: object | None = None,
    ) -> FlowDataset:
        """Validiert die Auswahl und verändert den bestehenden DataFrame."""
        if column_name not in dataset.dataframe.columns:
            raise MissingValueTreatmentError(
                f"Die Spalte '{column_name}' ist im Datensatz nicht vorhanden."
            )

        missing_rows = dataset.dataframe[column_name].isna()
        if not missing_rows.any():
            raise MissingValueTreatmentError(
                f"Die Spalte '{column_name}' enthält keine fehlenden Werte."
            )

        if operation not in {"remove", "replace"}:
            raise MissingValueTreatmentError("Die gewählte Behandlung ist ungültig.")

        value = replacement_value
        if operation == "replace":
            if replacement_value is None or replacement_value == "":
                raise MissingValueTreatmentError(
                    "Für die Ersetzung muss ein konstanter Wert angegeben werden."
                )
            if is_numeric_dtype(dataset.dataframe[column_name].dtype):
                try:
                    value = float(replacement_value)
                except (TypeError, ValueError) as error:
                    raise MissingValueTreatmentError(
                        "Der Ersatzwert für die numerische Spalte muss numerisch sein."
                    ) from error

        if operation == "remove":
            dataset.dataframe.drop(
                index=dataset.dataframe.index[missing_rows], inplace=True
            )
        else:
            dataset.dataframe.loc[missing_rows, column_name] = value

        dataset.refresh_metadata()
        return dataset
