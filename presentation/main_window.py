"""Hauptfenster der Desktopanwendung."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from application.calculate_statistics import CalculateStatistics
from application.exceptions import DatasetLoadError, StatisticsCalculationError
from application.flow_dataset import FlowDataset
from application.import_dataset import ImportDataset
from application.statistic_result import StatisticResult
from presentation.data_table_model import DataTableModel


def format_byte_size(size_bytes: int) -> str:
    """Formatiert eine Byte-Anzahl kompakt für die Benutzeroberfläche."""
    size = float(size_bytes)
    units = ("B", "KiB", "MiB", "GiB", "TiB")

    for unit in units[:-1]:
        if size < 1024:
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024

    return f"{size:.1f} {units[-1]}"


class MainWindow(QMainWindow):
    """Zeigt die Oberfläche zum Importieren eines CSV-Datensatzes."""

    def __init__(
        self,
        import_dataset: ImportDataset,
        calculate_statistics: CalculateStatistics,
    ) -> None:
        super().__init__()
        self._import_dataset = import_dataset
        self._calculate_statistics = calculate_statistics
        self._dataset: FlowDataset | None = None

        self.setWindowTitle("FlowWorkbench")
        self.resize(1200, 800)

        heading = QLabel("FlowWorkbench")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")

        import_button = QPushButton("Datensatz importieren")
        import_button.clicked.connect(self._select_and_import_dataset)

        self._statistics_button = QPushButton("Kennzahlen berechnen")
        self._statistics_button.setEnabled(False)
        self._statistics_button.clicked.connect(self._select_and_calculate_statistics)

        self._status_label = QLabel("Noch kein Datensatz geladen.")
        self._data_table = QTableView()
        self._data_table_model: DataTableModel | None = None

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(import_button)
        layout.addWidget(self._statistics_button)
        layout.addWidget(self._status_label)
        layout.addWidget(self._data_table, 1)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _select_and_import_dataset(self) -> None:
        """Öffnet den Dateidialog und importiert die ausgewählte CSV-Datei."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "CSV-Datei auswählen",
            "",
            "CSV-Dateien (*.csv)",
        )
        if not file_path:
            return

        self._status_label.setText("Noch kein Datensatz geladen.")
        self._dataset = None
        self._statistics_button.setEnabled(False)

        try:
            result = self._import_dataset.execute(Path(file_path))
        except DatasetLoadError as error:
            QMessageBox.critical(self, "Import fehlgeschlagen", str(error))
            return

        self._status_label.setText(
            f"Datei: {result.source.name}\n"
            f"Zeilen: {result.row_count}\n"
            f"Spalten: {result.column_count}\n"
            f"Speichergröße: {format_byte_size(result.memory_size_bytes)}\n"
            f"Fehlende Werte: {result.missing_value_count}\n"
            f"Unendliche Werte: {result.infinite_value_count}"
        )
        self._data_table_model = DataTableModel(result.preview)
        self._data_table.setModel(self._data_table_model)
        self._dataset = result
        self._statistics_button.setEnabled(True)

    def _select_and_calculate_statistics(self) -> None:
        """Lässt ein numerisches Merkmal auswählen und zeigt seine Kennzahlen."""
        if self._dataset is None:
            return

        numeric_features = list(
            self._dataset.dataframe.select_dtypes(include="number").columns
        )
        if not numeric_features:
            QMessageBox.information(
                self,
                "Keine numerischen Merkmale",
                "Der Datensatz enthält keine numerisch auswertbaren Merkmale.",
            )
            return

        feature_name, confirmed = QInputDialog.getItem(
            self,
            "Merkmal auswählen",
            "Numerisches Merkmal:",
            numeric_features,
            0,
            False,
        )
        if not confirmed:
            return

        try:
            result = self._calculate_statistics.execute(self._dataset, feature_name)
        except StatisticsCalculationError as error:
            QMessageBox.warning(self, "Berechnung nicht möglich", str(error))
            return

        QMessageBox.information(
            self,
            "Statistische Kennzahlen",
            self._format_statistics(result),
        )

    @staticmethod
    def _format_statistics(result: StatisticResult) -> str:
        """Formatiert ein Statistik-Ergebnis für die Anzeige."""
        return (
            f"Merkmal: {result.feature_name}\n"
            f"Minimum: {result.minimum:g}\n"
            f"Maximum: {result.maximum:g}\n"
            f"Mittelwert: {result.mean:g}\n"
            f"Median: {result.median:g}\n"
            f"Standardabweichung: {result.standard_deviation:g}"
        )
