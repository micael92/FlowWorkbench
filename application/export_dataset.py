"""Anwendungsfall zum Exportieren des aktuellen Datensatzes."""

from __future__ import annotations

from pathlib import Path

from application.exceptions import DatasetExportError
from application.flow_dataset import FlowDataset
from infrastructure.dataset_exporter import DatasetExporter


class ExportDataset:
    """Exportiert den aktuellen Bearbeitungsstand als CSV-Datei."""

    def __init__(self, exporter: DatasetExporter) -> None:
        self._exporter = exporter

    def execute(self, dataset: FlowDataset, path: Path) -> None:
        """Schreibt den DataFrame, ohne die ursprüngliche Datei zu überschreiben."""
        try:
            source_path = dataset.source.resolve()
            export_path = path.resolve()
        except OSError as error:
            raise DatasetExportError(
                f"Der Exportpfad ist ungültig: {path}"
            ) from error

        if source_path == export_path:
            raise DatasetExportError(
                "Die ursprüngliche Importdatei darf nicht überschrieben werden."
            )

        try:
            self._exporter.export_csv(dataset.dataframe, path)
        except OSError as error:
            raise DatasetExportError(
                f"Datensatz konnte nicht exportiert werden: {path}"
            ) from error
