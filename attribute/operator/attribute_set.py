import bpy
from gorgious_utilities.attribute.prop import set_attribute_ui


class GU_OT_attribute_set(bpy.types.Operator):
    bl_idname = "gu.attribute_set"
    bl_label = "Set attribute"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        active_object = context.active_object
        props = active_object.GUProps.attribute
        value = getattr(props, props.active_attribute.data_type)
        set_attribute_ui(props, value)

        return {"FINISHED"}
