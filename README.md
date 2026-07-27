# FlowWorkbench

FlowWorkbench ist eine Desktopanwendung zur Analyse, Vorverarbeitung und
Visualisierung von Netzwerkflussdaten.

## Voraussetzungen

- Python 3.12 oder neuer

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Anwendung starten

```powershell
python main.py
```

## Tests ausführen

```powershell
python -m pytest
```

## Architektur

- `presentation`: Benutzeroberfläche und Darstellung
- `application`: Anwendungsfälle und Ablaufsteuerung
- `domain`: Fachmodelle und Geschäftsregeln
- `infrastructure`: Datei-, Export- und Visualisierungsadapter
- `tests`: automatisierte Tests
