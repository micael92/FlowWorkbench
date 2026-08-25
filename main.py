"""Startpunkt der FlowWorkbench-Anwendung."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from application.calculate_label_distribution import CalculateLabelDistribution
from application.calculate_statistics import CalculateStatistics
from application.export_dataset import ExportDataset
from application.import_dataset import ImportDataset
from application.remove_features import RemoveFeatures
from application.treat_infinite_values import TreatInfiniteValues
from application.treat_missing_values import TreatMissingValues
from infrastructure.dataset_exporter import DatasetExporter
from infrastructure.dataset_loader import DatasetLoader
from presentation.main_window import MainWindow


def main() -> int:
    """Erzeugt und startet die FlowWorkbench-Anwendung."""
    app = QApplication(sys.argv)
    loader = DatasetLoader()
    import_dataset = ImportDataset(loader)
    calculate_statistics = CalculateStatistics()
    calculate_label_distribution = CalculateLabelDistribution()
    remove_features = RemoveFeatures()
    treat_missing_values = TreatMissingValues()
    treat_infinite_values = TreatInfiniteValues()
    exporter = DatasetExporter()
    export_dataset = ExportDataset(exporter)
    window = MainWindow(
        import_dataset,
        calculate_statistics,
        calculate_label_distribution,
        remove_features,
        export_dataset,
        treat_missing_values,
        treat_infinite_values,
    )
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
