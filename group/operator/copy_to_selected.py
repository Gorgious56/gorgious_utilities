from bpy.types import Operator
from bpy.props import StringProperty


class GU_OT_group_copy_to_selected(Operator):
    bl_idname = "group.copy_to_selected"
    bl_label = "Copy group value to selected"
    bl_options = {"UNDO", "REGISTER"}

    prop_name: StringProperty(name="Custom Property Name")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.prop_name and self.prop_name in context.active_object:
            group_from = context.active_object[self.prop_name]
            for obj in context.selected_objects:
                if obj == context.active_object:
                    continue
                obj[self.prop_name] = group_from
        return {"FINISHED"}
