import bpy
from gorgious_utilities.collection.helper import (
    get_family_down,
)
from gorgious_utilities.custom_property.helper import remove_trailing_numbers


class GU_OT_collection_rename_objects(bpy.types.Operator):
    """Rename each object in the collection"""

    bl_idname = "collection.rename_objects"
    bl_label = "Rename each object in the collection"
    bl_options = {"UNDO", "REGISTER"}

    replace_from: bpy.props.StringProperty(name="Replace")
    replace_to: bpy.props.StringProperty(name="With")
    as_collection: bpy.props.BoolProperty(name="Rename As Collection", default=True)
    recursive: bpy.props.BoolProperty(
        name="Recursive", description="Replace name in collection's children hierarchy", default=True
    )
    remove_trailing_numbers: bpy.props.BoolProperty(default=False, options={"SKIP_SAVE"})

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "recursive")
        layout.prop(self, "as_collection")
        col = layout.column()
        col.prop(self, "replace_from")
        col.prop(self, "replace_to")
        col.enabled = not self.as_collection

    def invoke(self, context, event):
        if self.remove_trailing_numbers:
            return self.execute(context)
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        cols = get_family_down(context.collection) if self.recursive else (context.collection,)
        for col in cols:            
            if self.remove_trailing_numbers:
                remove_trailing_numbers(col, "name")
            for obj in col.objects:
                if self.remove_trailing_numbers:
                    remove_trailing_numbers(obj, "name")
                else:
                    obj.name = col.name if self.as_collection else obj.name.replace(self.replace_from, self.replace_to)
                if hasattr(obj, "data") and obj.data is not None:
                    obj.data.name = obj.name

        return {"FINISHED"}
