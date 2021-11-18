import bpy
from gorgious_utilities.collection.helper import (
    get_family_down,
)


class GU_OT_collection_rename_objects(bpy.types.Operator):
    """Rename each object in the collection"""

    bl_idname = "collection.rename_objects"
    bl_label = "Rename each object in the collection"
    bl_options = {"UNDO", "REGISTER"}

    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="With")
    as_collection: bpy.props.BoolProperty(name="Rename As Collection", default=True)
    recursive: bpy.props.BoolProperty(name="Replace in children", default=True)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "recursive")
        layout.prop(self, "as_collection")
        col = layout.column()
        col.prop(self, "replace_from")
        col.prop(self, "replace_to")
        col.enabled = not self.as_collection

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        cols = get_family_down(context.collection) if self.recursive else (context.collection, )
        for col in cols:
            for obj in col.objects:
                obj.name = col.name
                if hasattr(obj, "data") and obj.data is not None:
                    obj.data.name = col.name

        return {"FINISHED"}
