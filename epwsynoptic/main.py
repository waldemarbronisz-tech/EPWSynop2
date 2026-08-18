import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer

from epwsynoptic.symbols.base import register_all_symbols
from epwsynoptic.ui.mainwindow import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setStyle("windows") # Retro style

    register_all_symbols()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
