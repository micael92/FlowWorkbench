"""Tests für das Tabellenmodell der Datenvorschau."""

import pandas as pd
from PySide6.QtCore import Qt

from presentation.data_table_model import DataTableModel


def test_data_table_model_returns_shape_and_display_values() -> None:
    dataframe = pd.DataFrame(
        {"source": ["A", "C"], "packets": [10, 20]}
    )
    model = DataTableModel(dataframe)

    assert model.rowCount() == 2
    assert model.columnCount() == 2
    assert model.data(model.index(0, 0)) == "A"
    assert model.data(model.index(1, 1)) == "20"


def test_data_table_model_uses_dataframe_columns_as_headers() -> None:
    model = DataTableModel(pd.DataFrame(columns=["source", "destination"]))

    assert model.headerData(0, Qt.Orientation.Horizontal) == "source"
    assert model.headerData(1, Qt.Orientation.Horizontal) == "destination"
