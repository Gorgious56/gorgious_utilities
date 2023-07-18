import bpy
from gorgious_utilities.modifier.helper import (
    get_geometry_nodes_groups_on_this_object,
)


class GU_OT_select_same_gn(bpy.types.Operator):
    bl_idname = "gu.select_same_gn"
    bl_label = "Select Same GN Tree"
    bl_options = {"REGISTER", "UNDO"}

    select_gn_tree: bpy.props.EnumProperty(
        items=get_geometry_nodes_groups_on_this_object, name="Select"
    )

    @classmethod
    def poll(cls, context):
        return (
            context.active_object
            and any(m for m in context.active_object.modifiers if m.type == "NODES")
            and len(get_geometry_nodes_groups_on_this_object(None, context)) > 0
        )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        for obj in bpy.data.objects:
            obj.select_set(False)
            for mod in obj.modifiers:
                if mod.type != "NODES":
                    continue
                if mod.node_group.name == self.select_gn_tree:
                    obj.select_set(True)
        if not context.active_object.select_get():
            context.view_layer.objects.active = None

        return {"FINISHED"}
