from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLabel, QFrame
from PySide6.QtCore import Qt, QMimeData
from PySide6.QtGui import QDrag
from epwsynoptic.runtime.tags import TagModel, Tag

class TagExplorerWidget(QWidget):
    def __init__(self, tag_model: TagModel, parent=None):
        super().__init__(parent)
        self.tag_model = tag_model

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Tags", "Value"])
        layout.addWidget(self.tree)

        # Populate mock devices
        self.populate_mock_devices()

    def populate_mock_devices(self):
        # ELA-01 (DI)
        ela_node = QTreeWidgetItem(["ELA-01"])
        di_node = QTreeWidgetItem(["Digital Inputs"])
        ela_node.addChild(di_node)
        for i in range(1, 33):
            tag_name = f"ELA01.DI{i:02d}"
            self.tag_model.add_tag(Tag(name=tag_name, value=False, data_type="bool"))
            item = QTreeWidgetItem([tag_name, "False"])
            item.setData(0, Qt.UserRole, tag_name)
            di_node.addChild(item)

        # ADA-01 (DO)
        ada_node = QTreeWidgetItem(["ADA-01"])
        do_node = QTreeWidgetItem(["Digital Outputs"])
        ada_node.addChild(do_node)
        for i in range(1, 33):
            tag_name = f"ADA01.DO{i:02d}"
            self.tag_model.add_tag(Tag(name=tag_name, value=False, data_type="bool"))
            item = QTreeWidgetItem([tag_name, "False"])
            item.setData(0, Qt.UserRole, tag_name)
            do_node.addChild(item)

        # EPM-01 (Energy)
        epm_node = QTreeWidgetItem(["EPM-01"])
        epm_tags = ["UL1", "UL2", "UL3", "IL1", "IL2", "IL3", "P", "Q", "S", "COSPHI", "FREQUENCY"]
        for t in epm_tags:
            tag_name = f"EPM01.{t}"
            self.tag_model.add_tag(Tag(name=tag_name, value=0.0, data_type="float"))
            item = QTreeWidgetItem([tag_name, "0.0"])
            item.setData(0, Qt.UserRole, tag_name)
            epm_node.addChild(item)

        self.tree.addTopLevelItems([ela_node, ada_node, epm_node])

    def mousePressEvent(self, event):
        item = self.tree.itemAt(event.position().toPoint())
        if item and item.data(0, Qt.UserRole):
            tag_name = item.data(0, Qt.UserRole)
            drag = QDrag(self)
            mime = QMimeData()
            mime.setText(f"TAG:{tag_name}")
            drag.setMimeData(mime)
            drag.exec(Qt.CopyAction)
        super().mousePressEvent(event)
