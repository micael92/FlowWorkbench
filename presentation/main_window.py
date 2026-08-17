"""Hauptfenster der Desktopanwendung."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from application.calculate_label_distribution import CalculateLabelDistribution
from application.calculate_statistics import CalculateStatistics
from application.exceptions import (
    DatasetExportError,
    DatasetLoadError,
    FeatureRemovalError,
    LabelDistributionError,
    StatisticsCalculationError,
)
from application.flow_dataset import FlowDataset
from application.export_dataset import ExportDataset
from application.import_dataset import ImportDataset
from application.remove_features import RemoveFeatures
from application.statistic_result import StatisticResult
from presentation.data_table_model import DataTableModel
from presentation.label_distribution_dialog import LabelDistributionDialog


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
        calculate_label_distribution: CalculateLabelDistribution,
        remove_features: RemoveFeatures,
        export_dataset: ExportDataset,
    ) -> None:
        super().__init__()
        self._import_dataset = import_dataset
        self._calculate_statistics = calculate_statistics
        self._calculate_label_distribution = calculate_label_distribution
        self._remove_features = remove_features
        self._export_dataset = export_dataset
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

        self._label_distribution_button = QPushButton(
            "Labelverteilung anzeigen"
        )
        self._label_distribution_button.setEnabled(False)
        self._label_distribution_button.clicked.connect(
            self._show_label_distribution
        )

        self._remove_features_button = QPushButton("Merkmale entfernen")
        self._remove_features_button.setEnabled(False)
        self._remove_features_button.clicked.connect(
            self._select_and_remove_features
        )

        self._export_button = QPushButton("Datensatz exportieren")
        self._export_button.setEnabled(False)
        self._export_button.clicked.connect(self._select_and_export_dataset)

        self._status_label = QLabel("Noch kein Datensatz geladen.")
        self._data_table = QTableView()
        self._data_table_model: DataTableModel | None = None
        self._data_table_proxy_model = QSortFilterProxyModel(self)
        self._data_table_proxy_model.setSortRole(DataTableModel.SORT_ROLE)
        self._data_table.setModel(self._data_table_proxy_model)
        self._data_table.setSortingEnabled(True)

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(import_button)
        layout.addWidget(self._statistics_button)
        layout.addWidget(self._label_distribution_button)
        layout.addWidget(self._remove_features_button)
        layout.addWidget(self._export_button)
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

        try:
            result = self._import_dataset.execute(Path(file_path))
        except DatasetLoadError as error:
            QMessageBox.critical(self, "Import fehlgeschlagen", str(error))
            return

        if result.label_column is None:
            label_column, confirmed = QInputDialog.getItem(
                self,
                "Label-Spalte auswählen",
                "Label-Spalte:",
                list(result.dataframe.columns),
                0,
                False,
            )
            if not confirmed:
                return
            result.label_column = label_column

        self._dataset = result
        self._statistics_button.setEnabled(True)
        self._label_distribution_button.setEnabled(True)
        self._remove_features_button.setEnabled(True)
        self._export_button.setEnabled(True)
        self._display_dataset()

    def _select_and_export_dataset(self) -> None:
        """Lässt einen Zielpfad auswählen und exportiert den aktuellen Datensatz."""
        if self._dataset is None:
            return

        suggested_path = self._dataset.source.with_name(
            f"{self._dataset.source.stem}_export.csv"
        )
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Datensatz exportieren",
            str(suggested_path),
            "CSV-Dateien (*.csv)",
        )
        if not file_path:
            return

        export_path = Path(file_path)
        if export_path.suffix.lower() != ".csv":
            export_path = Path(f"{export_path}.csv")

        try:
            self._export_dataset.execute(self._dataset, export_path)
        except DatasetExportError as error:
            QMessageBox.critical(self, "Export fehlgeschlagen", str(error))
            return

        QMessageBox.information(
            self,
            "Export erfolgreich",
            f"Der Datensatz wurde exportiert:\n{export_path}",
        )

    def _select_and_remove_features(self) -> None:
        """Lässt mehrere Merkmale auswählen und entfernt sie gemeinsam."""
        if self._dataset is None:
            return

        removable_features = [
            column
            for column in self._dataset.dataframe.columns
            if column != self._dataset.label_column
        ]
        if not removable_features:
            QMessageBox.information(
                self,
                "Keine entfernbaren Merkmale",
                "Der Datensatz enthält keine entfernbaren Merkmale.",
            )
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Merkmale entfernen")
        feature_list = QListWidget(dialog)
        for feature_name in removable_features:
            item = QListWidgetItem(str(feature_name), feature_list)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            parent=dialog,
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)

        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel("Zu entfernende Merkmale auswählen:"))
        layout.addWidget(feature_list)
        layout.addWidget(buttons)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        selected_features = [
            feature_list.item(index).text()
            for index in range(feature_list.count())
            if feature_list.item(index).checkState() == Qt.CheckState.Checked
        ]
        if not selected_features:
            return

        try:
            self._remove_features.execute(self._dataset, selected_features)
        except FeatureRemovalError as error:
            QMessageBox.warning(self, "Entfernen nicht möglich", str(error))
            return

        self._display_dataset()

    def _display_dataset(self) -> None:
        """Aktualisiert Datensatzinformationen und Vorschau."""
        if self._dataset is None:
            return

        self._status_label.setText(
            f"Datei: {self._dataset.source.name}\n"
            f"Zeilen: {self._dataset.row_count}\n"
            f"Spalten: {self._dataset.column_count}\n"
            "Speichergröße: "
            f"{format_byte_size(self._dataset.memory_size_bytes)}\n"
            f"Fehlende Werte: {self._dataset.missing_value_count}\n"
            f"Unendliche Werte: {self._dataset.infinite_value_count}"
        )
        self._data_table_model = DataTableModel(self._dataset.preview)
        self._data_table_proxy_model.setSourceModel(self._data_table_model)
        self._data_table_proxy_model.sort(-1)

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

    def _show_label_distribution(self) -> None:
        """Berechnet und zeigt die Verteilung der aktuellen Labels."""
        if self._dataset is None:
            return

        try:
            distribution = self._calculate_label_distribution.execute(self._dataset)
        except LabelDistributionError as error:
            QMessageBox.warning(self, "Anzeige nicht möglich", str(error))
            return

        dialog = LabelDistributionDialog(distribution, self)
        dialog.exec()

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
