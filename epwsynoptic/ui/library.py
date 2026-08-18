from PySide6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QLineEdit
from PySide6.QtCore import Qt, Signal
from epwsynoptic.core.registry import get_registry

class SymbolLibraryWidget(QWidget):
    symbol_selected = Signal(str) # Emits type_id

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search symbols...")
        self.search_box.textChanged.connect(self.filter_symbols)
        layout.addWidget(self.search_box)

        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.tree)

        self.populate_tree()

    def populate_tree(self):
        self.tree.clear()
        registry = get_registry()
        categories = {}

        for symbol in registry.get_all():
            if symbol.category not in categories:
                cat_item = QTreeWidgetItem([symbol.category])
                self.tree.addTopLevelItem(cat_item)
                categories[symbol.category] = cat_item

            item = QTreeWidgetItem([symbol.display_name])
            item.setData(0, Qt.UserRole, symbol.type_id)
            categories[symbol.category].addChild(item)

        self.tree.expandAll()

    def filter_symbols(self, text):
        text = text.lower()
        for i in range(self.tree.topLevelItemCount()):
            cat_item = self.tree.topLevelItem(i)
            cat_visible = False

            for j in range(cat_item.childCount()):
                child = cat_item.child(j)
                if text in child.text(0).lower():
                    child.setHidden(False)
                    cat_visible = True
                else:
                    child.setHidden(True)

            cat_item.setHidden(not cat_visible)

    def on_selection_changed(self):
        selected = self.tree.selectedItems()
        if selected and not selected[0].childCount(): # Ensure it's a leaf node
            type_id = selected[0].data(0, Qt.UserRole)
            self.symbol_selected.emit(type_id)
