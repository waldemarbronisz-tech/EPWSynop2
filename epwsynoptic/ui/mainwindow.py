from PySide6.QtWidgets import (
    QMainWindow, QDockWidget, QVBoxLayout, QWidget, QStatusBar, QToolBar,
    QMenuBar, QMenu, QFileDialog, QInputDialog, QGraphicsItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QUndoStack, QUndoGroup

from epwsynoptic.core.models import Page, Project
from epwsynoptic.core.registry import get_registry
from epwsynoptic.core.serialization import save_project, load_project
from epwsynoptic.core.commands import AddObjectCommand
from epwsynoptic.graphics.scene import EngineeringScene
from epwsynoptic.graphics.view import EngineeringView
from epwsynoptic.ui.library import SymbolLibraryWidget
from epwsynoptic.ui.preview import SymbolPreviewWidget
from epwsynoptic.ui.inspector import PropertyInspectorWidget
from epwsynoptic.ui.bottom_panel import BottomPanelWidget
from epwsynoptic.ui.tags import TagExplorerWidget
from epwsynoptic.runtime.tags import TagModel
from epwsynoptic.runtime.client import RuntimeClient

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tag_model = TagModel()
        self.runtime_client = RuntimeClient(self.tag_model)
        self.undo_stack = QUndoStack(self)

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

        self.tag_explorer = TagExplorerWidget(self.tag_model)
        self.bottom_widget.tags_tab.layout().addWidget(self.tag_explorer)

        self.bottom_dock.setWidget(self.bottom_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.bottom_dock)

        # Menu and Toolbar
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")

        open_action = QAction("Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.action_open_project)
        file_menu.addAction(open_action)

        save_action = QAction("Save Project...", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.action_save_project)
        file_menu.addAction(save_action)

        edit_menu = self.menu_bar.addMenu("Edit")
        undo_action = self.undo_stack.createUndoAction(self, "Undo")
        undo_action.setShortcut("Ctrl+Z")
        edit_menu.addAction(undo_action)

        redo_action = self.undo_stack.createRedoAction(self, "Redo")
        redo_action.setShortcut("Ctrl+Y")
        edit_menu.addAction(redo_action)

        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)

        self.mode_action = QAction("Switch to PREVIEW Mode", self)
        self.mode_action.triggered.connect(self.toggle_mode)
        self.toolbar.addAction(self.mode_action)
        self.current_mode = "EDIT"

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

    def setup_canvas(self):
        self.project = Project()
        self.current_page = Page(name="MAIN")
        self.project.pages.append(self.current_page)

        self.scene = EngineeringScene(self.current_page, self)
        self.view = EngineeringView(self.scene)
        self.setCentralWidget(self.view)

    def action_save_project(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save EPW Project", "", "EPW Synoptic Files (*.epwsyn)")
        if filepath:
            save_project(self.project, filepath)

    def action_open_project(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Open EPW Project", "", "EPW Synoptic Files (*.epwsyn)")
        if filepath:
            self.project = load_project(filepath)
            if self.project.pages:
                self.load_page(self.project.pages[0])
            self.update_status()

    def load_page(self, page):
        self.current_page = page
        self.scene = EngineeringScene(self.current_page, self)
        self.scene.selectionChangedSignal.connect(self.on_scene_selection_changed)

        registry = get_registry()
        for obj_model in self.current_page.objects:
            self.scene.add_engineering_object(obj_model)

        for conn_model in self.current_page.connections:
            self.scene.add_connection(conn_model)

        self.view.setScene(self.scene)
        self.view.setAcceptDrops(True)
        self.view.dragEnterEvent = self.dragEnterEvent_view
        self.view.dropEvent = self.dropEvent_view
        self.update_status()

    def setup_connections(self):
        self.library_widget.symbol_selected.connect(self.preview_widget.set_symbol)
        self.scene.selectionChangedSignal.connect(self.on_scene_selection_changed)
        self.view.zoom_changed.connect(self.on_zoom_changed)

        # Enable dropping on scene view
        self.view.setAcceptDrops(True)
        self.view.dragEnterEvent = self.dragEnterEvent_view
        self.view.dropEvent = self.dropEvent_view

    def toggle_mode(self):
        if self.current_mode == "EDIT":
            self.current_mode = "PREVIEW"
            self.mode_action.setText("Switch to EDIT Mode")
            # In preview mode, things aren't movable
            for item in self.scene.items():
                from epwsynoptic.graphics.items import BaseSymbolItem
                if isinstance(item, BaseSymbolItem):
                    item.setFlag(QGraphicsItem.ItemIsMovable, False)
                    item.setFlag(QGraphicsItem.ItemIsSelectable, False)
        else:
            self.current_mode = "EDIT"
            self.mode_action.setText("Switch to PREVIEW Mode")
            for item in self.scene.items():
                from epwsynoptic.graphics.items import BaseSymbolItem
                if isinstance(item, BaseSymbolItem):
                    item.setFlag(QGraphicsItem.ItemIsMovable, True)
                    item.setFlag(QGraphicsItem.ItemIsSelectable, True)

        self.scene.update()
        self.update_status()

    def dragEnterEvent_view(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent_view(self, event):
        text = event.mimeData().text()

        if text.startswith("TAG:"):
            tag_name = text.split("TAG:")[1]
            view_pos = event.position().toPoint()
            scene_pos = self.view.mapToScene(view_pos)
            item = self.scene.itemAt(scene_pos, self.view.transform())

            from epwsynoptic.graphics.items import BaseSymbolItem
            if isinstance(item, BaseSymbolItem):
                # We dropped on a symbol, bind it
                registry = get_registry()
                symbol_def = registry.get(item.model.type_id)
                if symbol_def and symbol_def.supported_bindings:
                    # Let user choose which property to bind to
                    binding_prop, ok = QInputDialog.getItem(self, "Bind Tag", "Bind to property:", symbol_def.supported_bindings, 0, False)
                    if ok and binding_prop:
                        item.model.bindings[binding_prop] = tag_name
                        self.inspector_widget.set_item(item) # refresh
            else:
                # Dropped on empty canvas, maybe create a measurement widget
                registry = get_registry()
                obj_model = registry.create_instance("automation.measurement")
                obj_model.x = scene_pos.x()
                obj_model.y = scene_pos.y()
                obj_model.bindings["value"] = tag_name
                obj_model.designation = tag_name.split(".")[-1]

                cmd = AddObjectCommand(self.scene, self.current_page, obj_model)
                self.undo_stack.push(cmd)
            event.accept()
            return

        type_id = text
        registry = get_registry()
        symbol_def = registry.get(type_id)

        if symbol_def:
            obj_model = registry.create_instance(type_id)

            # Map pos to scene pos
            view_pos = event.position().toPoint()
            scene_pos = self.view.mapToScene(view_pos)

            obj_model.x = scene_pos.x()
            obj_model.y = scene_pos.y()

            cmd = AddObjectCommand(self.scene, self.current_page, obj_model)
            self.undo_stack.push(cmd)

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
        mode_str = self.current_mode
        self.status_bar.showMessage(
            f"PROJECT: UNTITLED | PAGE: {self.current_page.name} | MODE: {mode_str} | "
            f"GRID: {self.current_page.grid_size} | SNAP: {grid_status} | ZOOM: {self.view.zoom_level}%"
        )
