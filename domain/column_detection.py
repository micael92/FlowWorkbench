"""Fachliche Regeln zur Erkennung relevanter Spalten."""

from __future__ import annotations


def detect_column(columns: list[str], candidates: tuple[str, ...]) -> str | None:
    """Liefert die erste Spalte, deren Name einem Kandidaten entspricht."""
    normalized = {column.casefold(): column for column in columns}
    return next(
        (normalized[name.casefold()] for name in candidates if name.casefold() in normalized),
        None,
    )
