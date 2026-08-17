"""Test für die fachliche Darstellung der Labelverteilung."""

import pandas as pd
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from PySide6.QtWidgets import QApplication, QTableWidget

from presentation.label_distribution_dialog import LabelDistributionDialog


def test_dialog_shows_numeric_distribution_and_bar_chart() -> None:
    app = QApplication.instance() or QApplication([])
    distribution = pd.DataFrame(
        {
            "label": ["BENIGN", "Attack", None],
            "count": [3, 1, 1],
            "percentage": [60.0, 20.0, 20.0],
        }
    )

    dialog = LabelDistributionDialog(distribution)
    table = dialog.findChild(QTableWidget)
    canvas = dialog.findChild(FigureCanvasQTAgg)

    assert table is not None
    assert table.rowCount() == 3
    assert table.item(0, 0).text() == "BENIGN"
    assert table.item(0, 1).text() == "3"
    assert table.item(0, 2).text() == "60.00 %"
    assert table.item(2, 0).text() == "Fehlend"
    assert canvas is not None
    assert len(canvas.figure.axes[0].patches) == 3

    dialog.close()
    app.processEvents()
