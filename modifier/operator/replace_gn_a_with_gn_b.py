import bpy
from gorgious_utilities.modifier.helper import (
    get_geometry_nodes_groups,
)

class GU_OT_modifier_replace_a_with_b(bpy.types.Operator):    
    bl_idname = "modifier.replace_gn_a_with_gn_b"
    bl_label = "Replace modifier"
    bl_options = {"REGISTER", "UNDO"}

    replace_from: bpy.props.EnumProperty(items=get_geometry_nodes_groups, name="Replace")
    replace_with: bpy.props.EnumProperty(items=get_geometry_nodes_groups, name="With")

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        replace_from = bpy.data.node_groups.get(self.replace_from)
        replace_with = bpy.data.node_groups.get(self.replace_with)
        if replace_from and replace_with and replace_with != replace_from:
            for obj in context.selected_objects:
                if not hasattr(obj, "modifiers"):
                    continue
                for mod in obj.modifiers:
                    if mod.type == "NODES" and mod.node_group == replace_from:
                        mod.node_group = replace_with

        return {"FINISHED"}

