import bpy
from gorgious_utilities.modifier.helper import (
    get_geometry_node_modifier_names,
    get_output_attributes,
)


class GU_OT_modifier_replace_a_with_b(bpy.types.Operator):
    bl_idname = "modifier.replace_output_name"
    bl_label = "Replace GN Output Name"
    bl_options = {"REGISTER", "UNDO"}

    mod_name: bpy.props.EnumProperty(items=get_geometry_node_modifier_names, name="Modifier Name")
    attribute_name: bpy.props.EnumProperty(items=get_output_attributes, name="Attribute Name")
    attribute_value: bpy.props.StringProperty(name="Attribute Value")

    @classmethod
    def poll(cls, context):
        return context.active_object and any(m for m in context.active_object.modifiers if m.type == "NODES")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        for obj in context.selected_objects:
            if not hasattr(obj, "modifiers"):
                continue
            mod = obj.modifiers.get(self.mod_name)
            if mod is None:
                continue
            mod[self.attribute_name] = self.attribute_value

        return {"FINISHED"}
