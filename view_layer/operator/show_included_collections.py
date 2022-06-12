import bpy
from gorgious_utilities.message.messagebox import show_message_box
from gorgious_utilities.view_layer.helper import get_view_layer_names
from gorgious_utilities.collection.tool import get_family_down


class GU_OT_view_layer_show_included(bpy.types.Operator):
    bl_label = "Show Included Collections"
    bl_idname = "view_layer.show_included"
    v_l_name: bpy.props.EnumProperty(
        items=lambda self, context: ((v_l_name,) * 3 for v_l_name in get_view_layer_names(context)),
        name="View Layer",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        included_collection_names = []
        view_layer = context.scene.view_layers.get(self.v_l_name)
        layer_col_main = view_layer.layer_collection
        for layer_col in get_family_down(layer_col_main):
            if not layer_col.exclude:
                included_collection_names.append(layer_col.name)
        included_collection_names.insert(0, f">> {len(included_collection_names)} included collections")
        show_message_box(context, included_collection_names)
        return {"FINISHED"}
