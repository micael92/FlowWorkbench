"""Startpunkt der FlowWorkbench-Anwendung."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from application.import_dataset import ImportDataset
from infrastructure.dataset_loader import DatasetLoader
from presentation.main_window import MainWindow


def main() -> int:
    """Erzeugt und startet die FlowWorkbench-Anwendung."""
    app = QApplication(sys.argv)
    loader = DatasetLoader()
    import_dataset = ImportDataset(loader)
    window = MainWindow(import_dataset)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
