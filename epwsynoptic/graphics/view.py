from PySide6.QtWidgets import QGraphicsView, QFrame
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPainter, QMouseEvent, QWheelEvent

class EngineeringView(QGraphicsView):
    zoom_changed = Signal(int)

    def __init__(self, scene=None, parent=None):
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

        # Disable scrollbars for a cleaner look unless needed
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.zoom_level = 100
        self.min_zoom = 10
        self.max_zoom = 500
        self.zoom_step = 10

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoom_in()
            else:
                self.zoom_out()
            event.accept()
        else:
            super().wheelEvent(event)

    def zoom_in(self):
        self._set_zoom(self.zoom_level + self.zoom_step)

    def zoom_out(self):
        self._set_zoom(self.zoom_level - self.zoom_step)

    def _set_zoom(self, level):
        level = max(self.min_zoom, min(self.max_zoom, level))
        if level != self.zoom_level:
            self.zoom_level = level
            scale_factor = self.zoom_level / 100.0
            self.resetTransform()
            self.scale(scale_factor, scale_factor)
            self.zoom_changed.emit(self.zoom_level)
