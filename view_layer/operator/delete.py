import bpy
from gorgious_utilities.view_layer.helper import delete_view_layer, get_view_layer_names


class GU_OT_view_layer_delete(bpy.types.Operator):
    bl_label = "Delete View Layer"
    bl_idname = "view_layer.delete"
    v_l_name: bpy.props.EnumProperty(
        items=lambda self, context: ((v_l_name,) * 3 for v_l_name in get_view_layer_names(context)),
        name="View Layer",
    )

    @classmethod
    def poll(cls, context):
        return len(context.scene.view_layers) > 1

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        delete_view_layer(context, self.v_l_name)
        return {"FINISHED"}
