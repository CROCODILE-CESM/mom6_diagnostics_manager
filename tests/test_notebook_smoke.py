from pathlib import Path

import ipywidgets as widgets
import pytest

from mom6_diagnostics_gui import create_diag_table_ui
from mom6_diagnostics_gui.ui.main_interface import DiagTableUI
import mom6_diagnostics_gui.ui.main_interface as main_interface


@pytest.mark.parametrize(
    "diag_file",
    [
        None,
        str(Path(__file__).resolve().parents[1] / "mom6_diagnostics_gui" / "data" / "available_diags.000000"),
    ],
)
def test_create_diag_table_ui_smoke(monkeypatch, diag_file):
    class FakePreviewExportUI:
        def __init__(self, *_args, **_kwargs):
            pass

        def get_preview_layout(self):
            return widgets.VBox()

        def get_export_layout(self):
            return widgets.VBox()

        def update_export_label(self):
            pass

    monkeypatch.setattr(main_interface, "display", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(main_interface, "PreviewExportUI", FakePreviewExportUI)

    ui = create_diag_table_ui(diag_file)

    assert isinstance(ui, DiagTableUI)
    assert ui.parser.diagnostics
