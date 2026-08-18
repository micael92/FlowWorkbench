"""Anwendungsspezifische Ausnahmen."""


class FlowWorkbenchError(Exception):
    """Basisklasse für erwartete Fehler der Anwendung."""


class DatasetLoadError(FlowWorkbenchError):
    """Ein Datensatz konnte nicht geladen werden."""


class DatasetExportError(FlowWorkbenchError):
    """Ein Datensatz konnte nicht exportiert werden."""


class StatisticsCalculationError(FlowWorkbenchError):
    """Statistische Kennzahlen konnten nicht berechnet werden."""


class FeatureRemovalError(FlowWorkbenchError):
    """Ausgewählte Merkmale konnten nicht entfernt werden."""


class MissingValueTreatmentError(FlowWorkbenchError):
    """Fehlende Werte konnten nicht behandelt werden."""


class InfiniteValueTreatmentError(FlowWorkbenchError):
    """Unendliche Werte konnten nicht behandelt werden."""


class LabelDistributionError(FlowWorkbenchError):
    """Die Labelverteilung konnte nicht berechnet werden."""
