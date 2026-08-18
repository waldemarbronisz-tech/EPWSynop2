from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag, QPixmap, QPainter, QColor
from epwsynoptic.core.registry import get_registry

class SymbolPreviewWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setMinimumHeight(150)

        layout = QVBoxLayout(self)
        self.name_label = QLabel("Select a symbol")
        self.name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.name_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.preview_label)

        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        layout.addWidget(self.info_label)

        self.current_type_id = None

    def set_symbol(self, type_id: str):
        self.current_type_id = type_id
        registry = get_registry()
        symbol = registry.get(type_id)

        if symbol:
            self.name_label.setText(symbol.display_name)
            self.info_label.setText(f"Ports: {len(symbol.ports)}\nStates: {', '.join(symbol.allowed_states)}")

            # Simple preview draw
            pixmap = QPixmap(100, 100)
            pixmap.fill(QColor("lightgray"))
            painter = QPainter(pixmap)
            painter.setPen(Qt.black)
            painter.drawRect(10, 10, 80, 80)
            painter.drawText(pixmap.rect(), Qt.AlignCenter, symbol.display_name)
            painter.end()

            self.preview_label.setPixmap(pixmap)
        else:
            self.name_label.setText("Select a symbol")
            self.preview_label.clear()
            self.info_label.clear()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.current_type_id:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.current_type_id)
            drag.setMimeData(mime_data)

            # Set drag image
            if self.preview_label.pixmap():
                drag.setPixmap(self.preview_label.pixmap())
                drag.setHotSpot(event.position().toPoint())

            drag.exec(Qt.CopyAction)
