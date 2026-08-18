from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPen, QColor
from epwsynoptic.graphics.items import BaseSymbolItem, PortItem
from epwsynoptic.graphics.connection import ConnectionItem

class EngineeringScene(QGraphicsScene):
    selectionChangedSignal = Signal()

    def __init__(self, page_model, parent=None):
        super().__init__(parent)
        self.page_model = page_model

        # Grid settings
        self.grid_enabled = self.page_model.grid_enabled
        self.grid_size = self.page_model.grid_size

        self.setSceneRect(0, 0, self.page_model.width, self.page_model.height)
        self.setBackgroundBrush(QColor(self.page_model.background))

        self.items_map = {}
        self.connection_items = []

        # Connection dragging state
        self.drawing_connection = False
        self.temp_connection_item = None
        self.start_port_item = None

        self.selectionChanged.connect(self._emit_selection_changed)

    def _emit_selection_changed(self):
        self.selectionChangedSignal.emit()

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        if not self.grid_enabled:
            return

        left = int(rect.left()) - (int(rect.left()) % int(self.grid_size))
        top = int(rect.top()) - (int(rect.top()) % int(self.grid_size))

        lines = []
        x = left
        while x < rect.right():
            lines.append((x, rect.top(), x, rect.bottom()))
            x += self.grid_size

        y = top
        while y < rect.bottom():
            lines.append((rect.left(), y, rect.right(), y))
            y += self.grid_size

        painter.setPen(QPen(QColor(220, 220, 220), 1))
        for line in lines:
            painter.drawLine(*line)

    def add_engineering_object(self, obj_model, item_class=BaseSymbolItem):
        item = item_class(obj_model)
        item.setPos(obj_model.x, obj_model.y)
        self.addItem(item)
        self.items_map[obj_model.id] = item
        return item

    def add_connection(self, conn_model):
        start_item = self.items_map.get(conn_model.fromObjectId)
        end_item = self.items_map.get(conn_model.toObjectId)

        item = ConnectionItem(conn_model, start_item, end_item)
        self.addItem(item)
        self.connection_items.append(item)
        item.update_route()
        return item

    def update_all_routes(self):
        for conn in self.connection_items:
            conn.update_route()

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())

        if isinstance(item, PortItem) and event.button() == Qt.LeftButton:
            self.drawing_connection = True
            self.start_port_item = item

            # Create a temporary visual connection
            from epwsynoptic.core.models import Connection
            temp_conn = Connection(
                id="temp",
                fromObjectId=item.parentItem().model.id,
                fromPort=item.port.id,
                toObjectId="",
                toPort="",
                domain=item.port.domain,
                medium=item.port.medium
            )
            self.temp_connection_item = ConnectionItem(temp_conn)
            self.addItem(self.temp_connection_item)

            # Start position
            start_pos = item.scenePos() + item.rect().center()
            self.temp_connection_item.start_pos = start_pos
            self.temp_connection_item.end_pos = event.scenePos()
            self.temp_connection_item.update_route()

            event.accept()
            return

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drawing_connection and self.temp_connection_item:
            self.temp_connection_item.end_pos = event.scenePos()
            self.temp_connection_item.update_route()
            event.accept()
            return

        super().mouseMoveEvent(event)

        # Update connections if objects are moving
        if self.mouseGrabberItem():
            self.update_all_routes()

    def mouseReleaseEvent(self, event):
        if self.drawing_connection:
            self.drawing_connection = False
            item_under_mouse = self.itemAt(event.scenePos(), self.views()[0].transform())

            if isinstance(item_under_mouse, PortItem) and item_under_mouse != self.start_port_item:
                target_port = item_under_mouse

                # Check compatibility
                if self.start_port_item.port.domain == target_port.port.domain:
                    # Create real connection
                    from epwsynoptic.core.models import Connection
                    import uuid
                    new_conn = Connection(
                        id=str(uuid.uuid4()),
                        fromObjectId=self.start_port_item.parentItem().model.id,
                        fromPort=self.start_port_item.port.id,
                        toObjectId=target_port.parentItem().model.id,
                        toPort=target_port.port.id,
                        domain=self.start_port_item.port.domain,
                        medium=self.start_port_item.port.medium
                    )
                    self.page_model.connections.append(new_conn)
                    self.add_connection(new_conn)

            # Remove temp line
            if self.temp_connection_item:
                self.removeItem(self.temp_connection_item)
                self.temp_connection_item = None

            self.start_port_item = None
            event.accept()
            return

        super().mouseReleaseEvent(event)
