import bpy
from bpy.props import EnumProperty, FloatVectorProperty, BoolProperty
from gorgious_utilities.nodes.helper import get_active_node_tree, get_node_types


class GU_OT_nodes_select_by_type(bpy.types.Operator):
    bl_idname = "nodes.select_by_type"
    bl_label = "Select all nodes of a given type"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        return get_active_node_tree(context) is not None

    node_type: EnumProperty(name="Type", items=get_node_types)
    execute_directly: BoolProperty(default=False)

    def invoke(self, context, event):
        if context.active_node is not None:
            self.node_type = context.active_node.type
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        node_type = self.node_type
        for node in get_active_node_tree(context).nodes:
            if node.type == node_type:
                node.select = True
        return {"FINISHED"}
