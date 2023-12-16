import bpy
from gorgious_utilities.attribute.prop import get_attribute_ui


class GU_OT_attribute_copy(bpy.types.Operator):
    bl_idname = "gu.attribute_copy"
    bl_label = "copy attribute"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def description(cls, context, properties):
        attribute = context.active_object.data.attributes.active
        props = context.active_object.GUProps.attribute
        value = getattr(props, attribute.data_type + "_copy")
        return f"Currently Stored Value\n{value}"

    def execute(self, context):
        attribute = context.active_object.data.attributes.active
        props = context.active_object.GUProps.attribute
        setattr(props, attribute.data_type + "_copy", get_attribute_ui(props))
        return {"FINISHED"}
