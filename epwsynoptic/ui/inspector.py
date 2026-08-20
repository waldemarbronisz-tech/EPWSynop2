from PySide6.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QCheckBox, QLabel
from PySide6.QtCore import Qt
from epwsynoptic.graphics.items import BaseSymbolItem

class PropertyInspectorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.layout.addLayout(self.form_layout)
        self.layout.addStretch()

        self.current_item = None

    def set_item(self, item):
        self.current_item = item
        self.clear()

        if not item:
            self.form_layout.addRow(QLabel("No selection"))
            return

        if isinstance(item, BaseSymbolItem):
            model = item.model

            self.desig_edit = QLineEdit(model.designation)
            self.desig_edit.textChanged.connect(self._on_desig_changed)
            self.form_layout.addRow("Designation", self.desig_edit)

            self.name_edit = QLineEdit(model.name)
            self.name_edit.textChanged.connect(self._on_name_changed)
            self.form_layout.addRow("Name", self.name_edit)

            self.show_desig_cb = QCheckBox()
            self.show_desig_cb.setChecked(model.label_settings.showDesignation)
            self.show_desig_cb.toggled.connect(self._on_show_desig_changed)
            self.form_layout.addRow("Show Desig", self.show_desig_cb)

            self.show_name_cb = QCheckBox()
            self.show_name_cb.setChecked(model.label_settings.showName)
            self.show_name_cb.toggled.connect(self._on_show_name_changed)
            self.form_layout.addRow("Show Name", self.show_name_cb)

            self.pos_combo = QComboBox()
            self.pos_combo.addItems(["TOP", "BOTTOM", "LEFT", "RIGHT"])
            self.pos_combo.setCurrentText(model.label_settings.position)
            self.pos_combo.currentTextChanged.connect(self._on_pos_changed)
            self.form_layout.addRow("Label Pos", self.pos_combo)

    def clear(self):
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def _on_desig_changed(self, text):
        if self.current_item:
            self.current_item.model.designation = text
            self.current_item.update_label()

    def _on_name_changed(self, text):
        if self.current_item:
            self.current_item.model.name = text
            self.current_item.update_label()

    def _on_show_desig_changed(self, checked):
        if self.current_item:
            self.current_item.model.label_settings.showDesignation = checked
            self.current_item.update_label()

    def _on_show_name_changed(self, checked):
        if self.current_item:
            self.current_item.model.label_settings.showName = checked
            self.current_item.update_label()

    def _on_pos_changed(self, text):
        if self.current_item:
            self.current_item.model.label_settings.position = text
            self.current_item.update_label()
