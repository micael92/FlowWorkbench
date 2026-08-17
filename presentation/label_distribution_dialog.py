"""Dialog für die numerische und grafische Anzeige der Labelverteilung."""

import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class LabelDistributionDialog(QDialog):
    """Zeigt eine Labelverteilung als Tabelle und Balkendiagramm."""

    def __init__(self, distribution: pd.DataFrame, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Labelverteilung")
        self.resize(800, 600)

        table = self._create_table(distribution)
        canvas = self._create_chart(distribution)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(table)
        layout.addWidget(canvas, 1)
        layout.addWidget(buttons)

    @classmethod
    def _create_table(cls, distribution: pd.DataFrame) -> QTableWidget:
        """Erzeugt die numerische Darstellung der Verteilung."""
        table = QTableWidget(len(distribution), 3)
        table.setHorizontalHeaderLabels(["Label", "Anzahl", "Anteil"])
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for row_index, row in distribution.iterrows():
            table.setItem(
                row_index, 0, QTableWidgetItem(cls._format_label(row["label"]))
            )
            table.setItem(row_index, 1, QTableWidgetItem(str(int(row["count"]))))
            table.setItem(
                row_index,
                2,
                QTableWidgetItem(f"{float(row['percentage']):.2f} %"),
            )

        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        return table

    @classmethod
    def _create_chart(cls, distribution: pd.DataFrame) -> FigureCanvasQTAgg:
        """Erzeugt ein horizontales Balkendiagramm für den Dialog."""
        labels = [cls._format_label(value) for value in distribution["label"]]
        counts = distribution["count"].astype(int)

        figure = Figure(figsize=(7, 4))
        axes = figure.add_subplot(111)
        axes.barh(labels, counts)
        axes.invert_yaxis()
        axes.set_title("Labelverteilung")
        axes.set_xlabel("Anzahl")
        figure.tight_layout()
        return FigureCanvasQTAgg(figure)

    @staticmethod
    def _format_label(value: object) -> str:
        """Formatiert fehlende und vorhandene Labelwerte für die Anzeige."""
        return "Fehlend" if pd.isna(value) else str(value)
