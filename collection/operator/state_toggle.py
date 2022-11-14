import bpy
from gorgious_utilities.collection.tool import get_collection_layers_from_collection


class GU_OT_collections_state_toggle(bpy.types.Operator):
    bl_idname = "gu.collections_state_toggle"
    bl_label = "Toggle All Collections States"
    bl_description = "Toggle state of all collections"
    bl_options = {"UNDO"}

    attribute: bpy.props.StringProperty()
    state: bpy.props.BoolProperty()

    def execute(self, context):
        layer_collection_main = context.view_layer.layer_collection
        for col in context.active_object.users_collection:
            for col_layer in get_collection_layers_from_collection(layer_collection_main, col):
                setattr(col_layer, self.attribute, self.state)
        return {"FINISHED"}
