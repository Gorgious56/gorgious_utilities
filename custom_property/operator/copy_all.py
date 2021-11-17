import bpy
from gorgious_utilities.custom_property.helper import (
    copy_all_custom_props,
)


class GU_OT_property_copy_all(bpy.types.Operator):
    """Copies all custom props from active to selected objects"""

    bl_idname = "property.copy_all"
    bl_label = "Copy ALL Props"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_editable_objects) > 1

    def execute(self, context):
        ao = context.active_object
        for ob in context.selected_editable_objects:
            if ob == ao:
                continue
            copy_all_custom_props(ao, ob)
        return {"FINISHED"}