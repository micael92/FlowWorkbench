"""Fachliche Datenmodelle."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Dataset:
    """Beschreibt einen in FlowWorkbench geladenen Datensatz."""

    source: Path
    columns: tuple[str, ...] = field(default_factory=tuple)
    row_count: int = 0
