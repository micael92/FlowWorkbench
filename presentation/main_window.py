"""Hauptfenster der Desktopanwendung."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from application.import_dataset import ImportDataset
from domain.exceptions import DatasetLoadError


class MainWindow(QMainWindow):
    """Zeigt die Oberfläche zum Importieren eines CSV-Datensatzes."""

    def __init__(self, import_dataset: ImportDataset) -> None:
        super().__init__()
        self._import_dataset = import_dataset

        self.setWindowTitle("FlowWorkbench")

        heading = QLabel("FlowWorkbench")
        heading.setStyleSheet("font-size: 24px; font-weight: bold;")

        import_button = QPushButton("Datensatz importieren")
        import_button.clicked.connect(self._select_and_import_dataset)

        self._status_label = QLabel("Noch kein Datensatz geladen.")

        layout = QVBoxLayout()
        layout.addWidget(heading)
        layout.addWidget(import_button)
        layout.addWidget(self._status_label)

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

        self._status_label.setText(
            f"Datei: {result.source.name}\n"
            f"Zeilen: {result.row_count}\n"
            f"Spalten: {result.column_count}"
        )
