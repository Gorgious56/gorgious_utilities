import bpy
from gorgious_utilities.collection.helper import get_family_down

class GU_OT_view_layer_toggle_layer_collections(bpy.types.Operator):
    bl_label = "Toggle all layer collections"
    bl_idname = "view_layer.toggle_layer_collections"
    action: bpy.props.EnumProperty(items=(
        ("ON", ) * 3, 
        ("OFF", ) * 3,
    ))

    def execute(self, context):
        exclude = True if self.action == "OFF" else False
        for layer_col in get_family_down(context.view_layer.layer_collection):
            layer_col.exclude = exclude
        return {"FINISHED"}
