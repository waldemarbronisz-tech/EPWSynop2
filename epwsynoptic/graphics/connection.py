from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtGui import QPainterPath, QPen, QColor
from PySide6.QtCore import Qt, QPointF
from epwsynoptic.core.models import Connection
from epwsynoptic.graphics.routing import route_orthogonal

class ConnectionItem(QGraphicsPathItem):
    def __init__(self, connection: Connection, start_item=None, end_item=None, parent=None):
        super().__init__(parent)
        self.connection_model = connection
        self.start_item = start_item
        self.end_item = end_item
        self.start_pos = QPointF(0, 0)
        self.end_pos = QPointF(0, 0)

        self.setZValue(-1) # Behind symbols

        pen = QPen(Qt.black, 2)
        if self.connection_model.domain == 'water':
            pen.setColor(QColor("blue"))
        elif self.connection_model.domain == 'hvac':
            pen.setColor(QColor("gray"))
            pen.setWidth(4)

        self.setPen(pen)
        self.setFlags(QGraphicsPathItem.ItemIsSelectable)

    def update_route(self):
        if self.start_item and self.end_item:
            # find port items to get exact positions
            start_port = None
            end_port = None
            for p in self.start_item.port_items:
                if p.port.id == self.connection_model.fromPort:
                    start_port = p
                    break
            for p in self.end_item.port_items:
                if p.port.id == self.connection_model.toPort:
                    end_port = p
                    break

            if start_port and end_port:
                self.start_pos = start_port.scenePos() + start_port.rect().center()
                self.end_pos = end_port.scenePos() + end_port.rect().center()

        # Calculate route
        points = route_orthogonal(self.start_pos, self.end_pos)

        path = QPainterPath()
        if points:
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)

        self.setPath(path)
