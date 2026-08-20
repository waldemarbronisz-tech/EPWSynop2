from PySide6.QtGui import QUndoCommand

class AddObjectCommand(QUndoCommand):
    def __init__(self, scene, page, obj_model, description="Add Object"):
        super().__init__(description)
        self.scene = scene
        self.page = page
        self.obj_model = obj_model
        self.item = None

    def redo(self):
        if self.obj_model not in self.page.objects:
            self.page.objects.append(self.obj_model)
        self.item = self.scene.add_engineering_object(self.obj_model)

    def undo(self):
        if self.obj_model in self.page.objects:
            self.page.objects.remove(self.obj_model)
        if self.item:
            self.scene.removeItem(self.item)
            if self.obj_model.id in self.scene.items_map:
                del self.scene.items_map[self.obj_model.id]
        # Also need to clean up any connections attached to this object (omitted for brevity here, but vital in prod)

class MoveObjectCommand(QUndoCommand):
    def __init__(self, item, old_pos, new_pos, description="Move Object"):
        super().__init__(description)
        self.item = item
        self.old_pos = old_pos
        self.new_pos = new_pos

    def redo(self):
        self.item.setPos(self.new_pos)
        self.item.model.x = self.new_pos.x()
        self.item.model.y = self.new_pos.y()
        # Since scene is accessible via item.scene(), trigger routing update
        if self.item.scene():
            self.item.scene().update_all_routes()

    def undo(self):
        self.item.setPos(self.old_pos)
        self.item.model.x = self.old_pos.x()
        self.item.model.y = self.old_pos.y()
        if self.item.scene():
            self.item.scene().update_all_routes()
