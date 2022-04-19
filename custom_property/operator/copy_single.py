import bpy
from gorgious_utilities.custom_property.helper import (
    copy_custom_prop,
    get_all_ui_props,
)


class GU_OT_property_copy_single(bpy.types.Operator):
    bl_idname = "property.copy_single"
    bl_label = "Copy ONE Custom Property"
    bl_description = "Copies a custom prop from active to selected objects"

    bl_options = {"UNDO"}

    prop_name: bpy.props.EnumProperty(
        name="Name", items=lambda self, context: ((p, p, p) for p in get_all_ui_props(context.active_object))
    )
    drive_prop: bpy.props.BoolProperty(name="Setup Driver")

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and len(context.selected_editable_objects) > 1

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        source = context.active_object
        for target in context.selected_editable_objects:
            if target == source:
                continue
            copy_custom_prop(source, target, self.prop_name, drive=self.drive_prop)
        return {"FINISHED"}
