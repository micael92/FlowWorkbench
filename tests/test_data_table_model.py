"""Tests für das Tabellenmodell der Datenvorschau."""

from pathlib import Path

import pandas as pd
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import QApplication

from application.flow_dataset import FlowDataset
from presentation.data_table_model import DataTableModel
from presentation.main_window import MainWindow


def create_sorting_proxy(dataframe: pd.DataFrame) -> QSortFilterProxyModel:
    """Erzeugt das für die Datenvorschau verwendete Sortiermodell."""
    source_model = DataTableModel(dataframe)
    proxy_model = QSortFilterProxyModel()
    proxy_model.setSourceModel(source_model)
    proxy_model.setSortRole(DataTableModel.SORT_ROLE)
    return proxy_model


def displayed_column(proxy_model: QSortFilterProxyModel, column: int) -> list[str]:
    """Liest eine sichtbare Spalte in ihrer aktuellen Reihenfolge aus."""
    return [
        proxy_model.data(proxy_model.index(row, column))
        for row in range(proxy_model.rowCount())
    ]


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


def test_proxy_sorts_numeric_values_ascending_and_descending() -> None:
    proxy_model = create_sorting_proxy(pd.DataFrame({"packets": [10, 2, 1]}))

    proxy_model.sort(0, Qt.SortOrder.AscendingOrder)
    assert displayed_column(proxy_model, 0) == ["1", "2", "10"]

    proxy_model.sort(0, Qt.SortOrder.DescendingOrder)
    assert displayed_column(proxy_model, 0) == ["10", "2", "1"]


def test_proxy_sorts_text_values() -> None:
    proxy_model = create_sorting_proxy(
        pd.DataFrame({"protocol": ["UDP", "ICMP", "TCP"]})
    )

    proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

    assert displayed_column(proxy_model, 0) == ["ICMP", "TCP", "UDP"]


def test_proxy_sorts_missing_values_without_error() -> None:
    proxy_model = create_sorting_proxy(
        pd.DataFrame({"duration": [3.0, None, 1.0, None]})
    )

    proxy_model.sort(0, Qt.SortOrder.AscendingOrder)
    ascending = displayed_column(proxy_model, 0)
    proxy_model.sort(0, Qt.SortOrder.DescendingOrder)
    descending = displayed_column(proxy_model, 0)

    expected_values = ["1.0", "3.0", "nan", "nan"]
    assert sorted(ascending) == sorted(descending) == expected_values
    assert ascending.count("nan") == 2
    assert descending.count("nan") == 2


def test_proxy_sort_keeps_preview_and_complete_dataframe_unchanged() -> None:
    dataframe = pd.DataFrame({"packets": [10, 2, 1], "Label": ["a", "b", "c"]})
    dataset = FlowDataset(
        source=Path("dataset.csv"),
        dataframe=dataframe,
        preview=dataframe.head(2),
        row_count=3,
        column_count=2,
        memory_size_bytes=0,
        missing_value_count=0,
        infinite_value_count=0,
        label_column="Label",
    )
    original_dataframe = dataset.dataframe.copy(deep=True)
    original_preview = dataset.preview.copy(deep=True)
    proxy_model = create_sorting_proxy(dataset.preview)

    proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

    assert displayed_column(proxy_model, 0) == ["2", "10"]
    pd.testing.assert_frame_equal(dataset.preview, original_preview)
    pd.testing.assert_frame_equal(dataset.dataframe, original_dataframe)


def test_main_window_uses_sortable_proxy_for_dataset_preview() -> None:
    app = QApplication.instance() or QApplication([])
    window = MainWindow(None, None, None, None, None)
    dataframe = pd.DataFrame({"packets": [10, 2, 1], "Label": ["a", "b", "c"]})
    window._dataset = FlowDataset(
        source=Path("dataset.csv"),
        dataframe=dataframe,
        preview=dataframe.head(1000),
        row_count=3,
        column_count=2,
        memory_size_bytes=0,
        missing_value_count=0,
        infinite_value_count=0,
        label_column="Label",
    )

    window._display_dataset()
    window._data_table.sortByColumn(0, Qt.SortOrder.AscendingOrder)

    assert window._data_table.isSortingEnabled()
    assert window._data_table.model() is window._data_table_proxy_model
    assert displayed_column(window._data_table_proxy_model, 0) == ["1", "2", "10"]

    window.close()
    app.processEvents()
