import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from epwsynoptic.symbols.base import register_all_symbols
from epwsynoptic.ui.mainwindow import MainWindow
from epwsynoptic.core.serialization import load_project

def capture_screenshots():
    app = QApplication(sys.argv)
    register_all_symbols()

    window = MainWindow()
    window.resize(1200, 800)

    proj = load_project("examples/ENTRY_GATE_DEMO.epwsyn")
    window.project = proj

    os.makedirs("screenshots", exist_ok=True)

    def grab(name):
        QApplication.processEvents()
        window.grab().save(f"screenshots/{name}.png")
        print(f"Saved {name}.png")

    # Re-run all just to be safe
    window.load_page(proj.pages[0])
    grab("1_main_interface")

    window.load_page(proj.pages[1])
    grab("2_power_page")

    window.preview_widget.set_symbol("electrical.disconnect_switch")
    grab("3_symbol_preview")

    grab("4_dynamic_busbar")

    window.load_page(proj.pages[2])
    grab("5_water_page")

    window.load_page(proj.pages[3])
    grab("6_hvac_page")

    window.load_page(proj.pages[5])
    grab("7_energy_page")

    window.bottom_dock.widget().setCurrentIndex(1)
    grab("8_tag_explorer")

    window.load_page(proj.pages[1])
    window.toggle_mode()
    for item in window.scene.items():
        from epwsynoptic.graphics.items import BaseSymbolItem
        if isinstance(item, BaseSymbolItem) and item.model.designation == "Q1":
            item.model.states = ["CLOSED"]
            item.update()
    grab("9_preview_mode")

capture_screenshots()
