"""Hauptfenster der Desktopanwendung."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from application.import_dataset import ImportDataset
from application.exceptions import DatasetLoadError
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

    def __init__(self, import_dataset: ImportDataset) -> None:
        super().__init__()
        self._import_dataset = import_dataset

        self.setWindowTitle("FlowWorkbench")
        self.resize(1200, 800)

        heading = QLabel("FlowWorkbench")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")

        import_button = QPushButton("Datensatz importieren")
        import_button.clicked.connect(self._select_and_import_dataset)

        self._status_label = QLabel("Noch kein Datensatz geladen.")
        self._data_table = QTableView()
        self._data_table_model: DataTableModel | None = None

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(import_button)
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
