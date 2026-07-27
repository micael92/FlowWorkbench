"""Tests für die Spaltenerkennung."""

from domain.column_detection import detect_column


def test_detect_column_ignores_case() -> None:
    assert detect_column(["Timestamp", "Source IP"], ("source ip",)) == "Source IP"


def test_detect_column_returns_none_for_unknown_column() -> None:
    assert detect_column(["Timestamp"], ("destination",)) is None
