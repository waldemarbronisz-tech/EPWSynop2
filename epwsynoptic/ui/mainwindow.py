from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QVBoxLayout, QWidget, QStatusBar, QToolBar,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from epwsynoptic.core.models import Page
from epwsynoptic.core.registry import get_registry
from epwsynoptic.graphics.scene import EngineeringScene
from epwsynoptic.graphics.view import EngineeringView
from epwsynoptic.ui.library import SymbolLibraryWidget
from epwsynoptic.ui.preview import SymbolPreviewWidget
from epwsynoptic.ui.inspector import PropertyInspectorWidget
from epwsynoptic.ui.bottom_panel import BottomPanelWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("EPW SYNOPTIC EDITOR - Ela Power Watch Engineering Environment")
        self.resize(1200, 800)

        # Style to look like classic windows engineering app
        self.setStyleSheet("""
            QMainWindow { background-color: #d4d0c8; }
            QDockWidget { border: 1px solid gray; }
            QDockWidget::title { background: #000080; color: white; padding: 2px; }
            QToolBar { border-bottom: 1px solid gray; }
        """)

        self.setup_ui()
        self.setup_canvas()
        self.setup_connections()
        self.update_status()

    def setup_ui(self):
        # Library Dock
        self.library_dock = QDockWidget("SYMBOL LIBRARY", self)
        self.library_widget = SymbolLibraryWidget()

        # Preview Dock (placed under library)
        self.preview_dock = QDockWidget("SYMBOL PREVIEW", self)
        self.preview_widget = SymbolPreviewWidget()
        self.preview_dock.setWidget(self.preview_widget)

        # Layout for left side
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.addWidget(self.library_widget)
        self.library_dock.setWidget(left_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.library_dock)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.preview_dock)

        # Inspector Dock
        self.inspector_dock = QDockWidget("PROPERTY INSPECTOR", self)
        self.inspector_widget = PropertyInspectorWidget()
        self.inspector_dock.setWidget(self.inspector_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, self.inspector_dock)

        # Bottom Panel Dock
        self.bottom_dock = QDockWidget("PANELS", self)
        self.bottom_widget = BottomPanelWidget()
        self.bottom_dock.setWidget(self.bottom_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)

        # Menu and Toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def setup_canvas(self):
        self.current_page = Page(name="MAIN")
        self.scene = EngineeringScene(self.current_page, self)
        self.view = EngineeringView(self.scene)
        self.setCentralWidget(self.view)

    def setup_connections(self):
        self.library_widget.symbol_selected.connect(self.preview_widget.set_symbol)
        self.scene.selectionChangedSignal.connect(self.on_scene_selection_changed)
        self.view.zoom_changed.connect(self.on_zoom_changed)

        # Enable dropping on scene view
        self.view.setAcceptDrops(True)
        self.view.dragEnterEvent = self.dragEnterEvent_view
        self.view.dropEvent = self.dropEvent_view

    def dragEnterEvent_view(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent_view(self, event):
        type_id = event.mimeData().text()
        registry = get_registry()
        symbol_def = registry.get(type_id)

        if symbol_def:
            obj_model = registry.create_instance(type_id)

            # Map pos to scene pos
            view_pos = event.position().toPoint()
            scene_pos = self.view.mapToScene(view_pos)

            obj_model.x = scene_pos.x()
            obj_model.y = scene_pos.y()

            self.current_page.objects.append(obj_model)
            self.scene.add_engineering_object(obj_model)

            event.accept()

    def on_scene_selection_changed(self):
        selected = self.scene.selectedItems()
        from epwsynoptic.graphics.items import BaseSymbolItem

        # Only show properties for BaseSymbolItem for now
        valid_items = [item for item in selected if isinstance(item, BaseSymbolItem)]

        if valid_items:
            self.inspector_widget.set_item(valid_items[0])
        else:
            self.inspector_widget.set_item(None)

    def on_zoom_changed(self, level):
        self.update_status()

    def update_status(self):
        grid_status = "ON" if self.current_page.grid_enabled else "OFF"
        self.status_bar.showMessage(
            f"PROJECT: UNTITLED | PAGE: {self.current_page.name} | MODE: EDIT | "
            f"GRID: {self.current_page.grid_size} | SNAP: {grid_status} | ZOOM: {self.view.zoom_level}%"
        )
