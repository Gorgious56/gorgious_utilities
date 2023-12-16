import bpy
from gorgious_utilities.attribute.prop import set_attribute_ui


class GU_OT_attribute_paste(bpy.types.Operator):
    bl_idname = "gu.attribute_paste"
    bl_label = "Paste Attribute"
    bl_options = {"UNDO", "REGISTER"}

    def execute(self, context):
        attribute = context.active_object.data.attributes.active
        props = context.active_object.GUProps.attribute
        value = getattr(props, attribute.data_type + "_copy")
        set_attribute_ui(None, value)

        return {"FINISHED"}
