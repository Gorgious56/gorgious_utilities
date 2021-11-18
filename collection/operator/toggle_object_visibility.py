import bpy
from gorgious_utilities.collection.helper import (
    get_family_down,
)


class GU_OT_collection_toggle_object_viewport(bpy.types.Operator):
    """Toggle Visibility of Boolean Collections"""

    bl_idname = "collection.toggle_objects_viewport"
    bl_label = "Toggle Boolean Viewport Visibility"
    bl_options = {"UNDO"}

    col_name: bpy.props.StringProperty(name="Col Name", default="BOOL")

    def execute(self, context):
        cols = [c for c in bpy.data.collections if self.col_name.lower() in c.name.lower()]
        if cols:
            exclude = None
            layer_collections = get_family_down(context.view_layer.layer_collection)
            layer_collections_collections = [l_c.collection for l_c in layer_collections]
            for i, col in enumerate(cols):
                index = layer_collections_collections.index(col)
                if i == 0:
                    exclude = not layer_collections[index].exclude
                layer_collections[index].exclude = exclude

        return {"FINISHED"}

