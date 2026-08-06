# FlowWorkbench

FlowWorkbench ist eine unter Windows lauffähige Desktopanwendung zur Analyse,
Visualisierung und Vorverarbeitung flowbasierter Netzwerkdatensätze.

Die Anwendung richtet sich insbesondere an Forschende, Studierende und
Entwickler, die mit Datensätzen für Machine-Learning-basierte Intrusion
Detection Systeme arbeiten. Ziel ist es, bereits erzeugte Netzwerkflussdaten
über eine grafische Benutzeroberfläche zu untersuchen, aufzubereiten und für
nachgelagerte Verarbeitungsschritte zu exportieren.

## Projektziel

FlowWorkbench unterstützt die Arbeit mit flowbasierten Netzwerkdatensätzen
durch folgende Kernfunktionen:

- Import von Datensätzen im CSV-Format
- Anzeige grundlegender Datensatzinformationen
- tabellarische Vorschau der geladenen Daten
- Berechnung statistischer Kennzahlen
- Darstellung der Labelverteilung
- Visualisierung ausgewählter Merkmale
- Erkennung und Behandlung fehlender oder unendlicher Werte
- Entfernung ungeeigneter oder ausgewählter Features
- Export verarbeiteter Datensätze im CSV-Format

Die Anwendung ist ausdrücklich:

- kein Intrusion Detection System,
- kein Packet Sniffer,
- kein Werkzeug zur Aufzeichnung von Netzwerkverkehr,
- kein Flow-Generator,
- kein System zum Training von Machine-Learning-Modellen.

FlowWorkbench verarbeitet bereits vorhandene flowbasierte Datensätze.

## Architektur

Die Anwendung verwendet eine Schichtenarchitektur mit vier Bereichen:

```text
presentation
     │
     ▼
application
     │
     ▼
domain

infrastructure ── implementiert technische Adapter und Ports
```

Die Schichten besitzen klar voneinander getrennte Verantwortlichkeiten. Die Schichten dienen der übersichtlichen Trennung der Verantwortlichkeiten.
Dabei wird bewusst keine vollständig strikte Clean-Architecture-Umsetzung
angestrebt. Für den begrenzten Projektumfang werden einfache und verständliche
Lösungen bevorzugt.

| Schicht | Verantwortung |
|---|---|
| `presentation` | Grafische Benutzeroberfläche, Dialoge und Darstellung |
| `application` | Anwendungsfälle, Ablaufsteuerung und Koordination |
| `domain` | Fachmodelle, fachliche Regeln und technologieunabhängige Logik |
| `infrastructure` | Technische Adapter für Dateien, Datenverarbeitung und Visualisierung |
| `tests` | Automatisierte Tests der Anwendung |

Technische Details und Architekturentscheidungen werden in
[`DECISIONS.md`](DECISIONS.md) dokumentiert.

## Projektstruktur

```text
FlowWorkbench/
├── application/
├── domain/
├── infrastructure/
├── presentation/
├── tests/
├── sample_data/
├── docs/
│   └── phase1/
├── AGENTS.md
├── DECISIONS.md
├── LICENSE
├── main.py
├── pyproject.toml
└── README.md
```

## Voraussetzungen

- Python 3.12 oder neuer
- Windows 10 oder Windows 11

## Installation

Eine virtuelle Python-Umgebung wird empfohlen.

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

## Verwendete Technologien

Der aktuelle Technologie-Stack umfasst insbesondere:

- Python
- PySide6
- pandas
- Matplotlib
- pytest
- Git und GitHub

Weitere Bibliotheken werden nur ergänzt, wenn sie für eine konkrete
Anforderung erforderlich sind. Die endgültige Technologieübersicht wird im
Architekturdokument auf Grundlage der tatsächlich eingesetzten Technologien
erstellt.

## Entwicklungsprozess

Die Entwicklung erfolgt iterativ und in kleinen, nachvollziehbaren Schritten.

Für neue Funktionen gilt grundsätzlich:

1. Anforderung und fachlichen Zweck klären.
2. betroffenen Anwendungsfall bestimmen.
3. Verantwortlichkeiten den Schichten zuordnen.
4. Funktion möglichst klein implementieren.
5. automatisierte Tests ergänzen.
6. Ergebnis manuell prüfen.
7. relevante Entscheidungen dokumentieren.

KI-Werkzeuge und Coding-Agenten können die Implementierung, Fehlersuche,
Codeanalyse und Testerstellung unterstützen. Architekturentscheidungen,
Anforderungsprüfung und Verantwortung für den übernommenen Code verbleiben
beim Projektverantwortlichen.