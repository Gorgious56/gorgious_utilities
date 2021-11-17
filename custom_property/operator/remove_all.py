import bpy


class GU_OT_remove_custom_props(bpy.types.Operator):
    """Removes all custom properties from selected objects"""

    bl_idname = "object.remove_all_custom_props"
    bl_label = "Remove All Properties"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_editable_objects) > 0

    def execute(self, context):
        for obj in context.selected_editable_objects:
            props = [*obj.keys()]
            for i in range(len(props) - 1, -1, -1):
                del obj[props[i]]
        return {"FINISHED"}
