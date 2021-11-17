import bpy

from gorgious_utilities.modifier.helper import (
    copy_modifiers,
)


class GU_OT_modifier_drive(bpy.types.Operator):
    """Drive Modifiers"""

    bl_idname = "modifier.drive"
    bl_label = "Drive"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        selected_objects = context.view_layer.objects.selected
        selected_object = context.object
        if not (selected_object and selected_objects):
            return
        copy_modifiers(selected_object, selected_objects, replace=False, drive=True)
        return {"FINISHED"}
