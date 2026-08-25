"""Tests für den Export des aktuellen Datensatzes."""

from pathlib import Path

import pandas as pd
import pytest

from application.exceptions import DatasetExportError
from application.export_dataset import ExportDataset
from application.flow_dataset import FlowDataset
from application.remove_features import RemoveFeatures
from infrastructure.dataset_exporter import DatasetExporter


class RecordingExporter(DatasetExporter):
    """Zeichnet den Aufruf auf, ohne eine Datei zu schreiben."""

    def __init__(self) -> None:
        self.dataframe: pd.DataFrame | None = None
        self.path: Path | None = None

    def export_csv(self, dataframe: pd.DataFrame, path: Path) -> None:
        self.dataframe = dataframe
        self.path = path


def create_dataset(source: Path, dataframe: pd.DataFrame) -> FlowDataset:
    """Erzeugt einen kleinen FlowDataset für die Exporttests."""
    return FlowDataset(
        source=source,
        dataframe=dataframe,
        preview=dataframe.head(1000),
        row_count=len(dataframe),
        column_count=len(dataframe.columns),
        memory_size_bytes=0,
        missing_value_count=0,
        infinite_value_count=0,
        label_column="Label",
    )


def test_export_writes_complete_dataframe_without_index(tmp_path: Path) -> None:
    dataframe = pd.DataFrame(
        {"Duration": [1, 2], "Label": ["normal", "attack"]},
        index=[10, 20],
    )
    dataset = create_dataset(tmp_path / "source.csv", dataframe)
    export_path = tmp_path / "export.csv"

    ExportDataset(DatasetExporter()).execute(dataset, export_path)

    exported = pd.read_csv(export_path)
    pd.testing.assert_frame_equal(exported, dataframe.reset_index(drop=True))


def test_export_uses_dataframe_after_feature_removal(tmp_path: Path) -> None:
    dataframe = pd.DataFrame(
        {"Flow ID": ["a"], "Duration": [1], "Label": ["normal"]}
    )
    dataset = create_dataset(tmp_path / "source.csv", dataframe)
    RemoveFeatures().execute(dataset, ["Flow ID"])

    export_path = tmp_path / "export.csv"
    ExportDataset(DatasetExporter()).execute(dataset, export_path)

    exported = pd.read_csv(export_path)
    assert list(exported.columns) == ["Duration", "Label"]


def test_export_uses_injected_exporter(tmp_path: Path) -> None:
    dataframe = pd.DataFrame({"Duration": [1], "Label": ["normal"]})
    dataset = create_dataset(tmp_path / "source.csv", dataframe)
    export_path = tmp_path / "export.csv"
    exporter = RecordingExporter()

    ExportDataset(exporter).execute(dataset, export_path)

    assert exporter.dataframe is dataframe
    assert exporter.path == export_path


def test_export_rejects_equivalent_source_path_and_preserves_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "source.csv"
    original_content = "Duration,Label\n1,normal\n"
    source.write_text(original_content, encoding="utf-8")
    dataset = create_dataset(source, pd.DataFrame({"changed": [99]}))
    monkeypatch.chdir(tmp_path)

    with pytest.raises(DatasetExportError, match="nicht überschrieben"):
        ExportDataset(DatasetExporter()).execute(dataset, Path("source.csv"))

    assert source.read_text(encoding="utf-8") == original_content


def test_export_translates_technical_write_error(tmp_path: Path) -> None:
    dataframe = pd.DataFrame({"Duration": [1], "Label": ["normal"]})
    dataset = create_dataset(tmp_path / "source.csv", dataframe)
    invalid_path = tmp_path / "missing-directory" / "export.csv"

    with pytest.raises(DatasetExportError, match="konnte nicht exportiert"):
        ExportDataset(DatasetExporter()).execute(dataset, invalid_path)


def test_export_does_not_mutate_dataframe(tmp_path: Path) -> None:
    dataframe = pd.DataFrame({"Duration": [1], "Label": ["normal"]})
    dataset = create_dataset(tmp_path / "source.csv", dataframe)
    original_dataframe = dataframe.copy(deep=True)
    original_object = dataset.dataframe

    ExportDataset(DatasetExporter()).execute(dataset, tmp_path / "export.csv")

    assert dataset.dataframe is original_object
    pd.testing.assert_frame_equal(dataset.dataframe, original_dataframe)
