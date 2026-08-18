from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel

class BottomPanelWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.pages_tab = QWidget()
        self.pages_tab.setLayout(QVBoxLayout())
        self.pages_tab.layout().addWidget(QLabel("Pages management..."))
        self.addTab(self.pages_tab, "Pages")

        self.tags_tab = QWidget()
        self.tags_tab.setLayout(QVBoxLayout())
        self.tags_tab.layout().addWidget(QLabel("Tag explorer..."))
        self.addTab(self.tags_tab, "Tags")

        self.bindings_tab = QWidget()
        self.bindings_tab.setLayout(QVBoxLayout())
        self.bindings_tab.layout().addWidget(QLabel("Bindings overview..."))
        self.addTab(self.bindings_tab, "Bindings")

        self.warnings_tab = QWidget()
        self.warnings_tab.setLayout(QVBoxLayout())
        self.warnings_tab.layout().addWidget(QLabel("Validation warnings..."))
        self.addTab(self.warnings_tab, "Warnings")

        self.runtime_tab = QWidget()
        self.runtime_tab.setLayout(QVBoxLayout())
        self.runtime_tab.layout().addWidget(QLabel("Runtime status..."))
        self.addTab(self.runtime_tab, "Runtime")
