"""Tabellenmodell für die Darstellung geladener Datensätze."""

from __future__ import annotations

import pandas as pd
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt


class DataTableModel(QAbstractTableModel):
    """Stellt die Werte eines DataFrames in einer Qt-Tabelle dar."""

    SORT_ROLE = Qt.ItemDataRole.UserRole

    def __init__(self, dataframe: pd.DataFrame) -> None:
        super().__init__()
        self._dataframe = dataframe

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._dataframe.columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        value = self._dataframe.iat[index.row(), index.column()]
        if role == Qt.ItemDataRole.DisplayRole:
            return str(value)
        if role == self.SORT_ROLE:
            if pd.isna(value):
                return None
            return value.item() if hasattr(value, "item") else value
        return None

    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return str(self._dataframe.columns[section])
        return super().headerData(section, orientation, role)
