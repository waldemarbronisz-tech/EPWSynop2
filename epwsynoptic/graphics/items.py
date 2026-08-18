from PySide6.QtWidgets import QGraphicsItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPen, QBrush, QColor, QFont
from epwsynoptic.core.models import EngineeringObject, Port

class PortItem(QGraphicsRectItem):
    def __init__(self, port: Port, parent=None):
        super().__init__(-3, -3, 6, 6, parent)
        self.port = port
        self.setBrush(QBrush(QColor("black")))
        self.setPen(QPen(Qt.NoPen))
        self.setAcceptHoverEvents(True)
        self.hide() # Hidden by default

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor("red")))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor("black")))
        super().hoverLeaveEvent(event)

class BaseSymbolItem(QGraphicsItem):
    def __init__(self, model: EngineeringObject, parent=None):
        super().__init__(parent)
        self.model = model

        self.setFlags(
            QGraphicsItem.ItemIsSelectable |
            QGraphicsItem.ItemIsMovable |
            QGraphicsItem.ItemSendsGeometryChanges
        )
        self.setAcceptHoverEvents(True)

        self.port_items = []
        for port in self.model.ports:
            # create ports
            p_item = PortItem(port, self)
            p_item.setPos(port.x * self.model.width, port.y * self.model.height)
            self.port_items.append(p_item)

        self.label_item = QGraphicsTextItem(self)
        self.update_label()

    def boundingRect(self):
        return QRectF(0, 0, self.model.width, self.model.height)

    def paint(self, painter, option, widget):
        # Override this in subclasses
        rect = self.boundingRect()

        pen = QPen(Qt.black)
        if self.isSelected():
            pen.setStyle(Qt.DashLine)
            pen.setColor(QColor("blue"))

        painter.setPen(pen)
        painter.drawRect(rect)

    def hoverEnterEvent(self, event):
        for p in self.port_items:
            p.show()
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        for p in self.port_items:
            p.hide()
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            self.model.x = self.pos().x()
            self.model.y = self.pos().y()
            # We'll emit a signal or notify scene later for routing updates
        return super().itemChange(change, value)

    def update_label(self):
        settings = self.model.label_settings
        texts = []
        if settings.showDesignation and self.model.designation:
            texts.append(self.model.designation)
        if settings.showName and self.model.name:
            texts.append(self.model.name)

        if texts:
            self.label_item.setPlainText("\n".join(texts))
            self.label_item.show()

            # Position logic
            rect = self.boundingRect()
            l_rect = self.label_item.boundingRect()

            if settings.position == "TOP":
                self.label_item.setPos(rect.width() / 2 - l_rect.width() / 2, -l_rect.height() - 5)
            elif settings.position == "BOTTOM":
                self.label_item.setPos(rect.width() / 2 - l_rect.width() / 2, rect.height() + 5)
            elif settings.position == "LEFT":
                self.label_item.setPos(-l_rect.width() - 5, rect.height() / 2 - l_rect.height() / 2)
            elif settings.position == "RIGHT":
                self.label_item.setPos(rect.width() + 5, rect.height() / 2 - l_rect.height() / 2)
        else:
            self.label_item.hide()
