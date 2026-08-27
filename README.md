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

Die Anwendung verwendet eine Schichtenarchitektur mit drei Bereichen:

| Schicht | Verantwortung |
|---|---|
| `presentation` | Grafische Benutzeroberfläche, Dialoge, Darstellung und Erzeugung der GUI-Diagramme |
| `application` | Anwendungsfälle, Ergebnisobjekte, Ablaufsteuerung und anwendungsbezogene Fehler |
| `infrastructure` | Dateizugriff sowie technische Umsetzung von Import und Export |

Die Schichten besitzen klar voneinander getrennte Verantwortlichkeiten. Die Schichten dienen der übersichtlichen Trennung der Verantwortlichkeiten.
Dabei wird bewusst keine vollständig strikte Clean-Architecture-Umsetzung
angestrebt. Für den begrenzten Projektumfang werden einfache und verständliche
Lösungen bevorzugt.

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
