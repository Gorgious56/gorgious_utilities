from bpy.types import Operator
from bpy.props import IntProperty, StringProperty


class GU_OT_group_by_custom_prop(Operator):
    bl_idname = "group.by_custom_prop"
    bl_label = "Group with a common custom prop"
    bl_options = {"UNDO", "REGISTER"}

    prop_name: StringProperty(name="Custom Property Name")
    group_value: IntProperty(name="Group")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        if self.prop_name:
            for obj in context.selected_objects:
                obj[self.prop_name] = self.group_value
        return {"FINISHED"}
