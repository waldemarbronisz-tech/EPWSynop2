import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from epwsynoptic.symbols.base import register_all_symbols
from epwsynoptic.ui.mainwindow import MainWindow

def test():
    app = QApplication(sys.argv)
    register_all_symbols()
    window = MainWindow()
    # Don't show, just instantiate to make sure imports and setup pass without xcb errors
    print("MainWindow instantiated successfully.")

if __name__ == "__main__":
    test()
