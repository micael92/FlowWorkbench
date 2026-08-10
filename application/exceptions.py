"""Anwendungsspezifische Ausnahmen."""


class FlowWorkbenchError(Exception):
    """Basisklasse für erwartete Fehler der Anwendung."""


class DatasetLoadError(FlowWorkbenchError):
    """Ein Datensatz konnte nicht geladen werden."""


class DatasetExportError(FlowWorkbenchError):
    """Ein Datensatz konnte nicht exportiert werden."""
