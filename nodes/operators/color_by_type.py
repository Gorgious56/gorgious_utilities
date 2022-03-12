import bpy
from bpy.props import EnumProperty, FloatVectorProperty, BoolProperty
from gorgious_utilities.nodes.helper import get_active_node_tree, get_node_types


class GU_OT_nodes_color_by_type(bpy.types.Operator):
    bl_idname = "nodes.color_by_type"
    bl_label = "Color all nodes of a given type"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        return get_active_node_tree(context) is not None

    node_type: EnumProperty(name="Type", items=get_node_types)
    node_color: FloatVectorProperty(name="Color", subtype="COLOR", min=0, max=1, default=(0.5, 0.5, 0.5))
    select_nodes: BoolProperty(name="Select nodes after operation", default=False)

    def invoke(self, context, event):
        if context.active_node is not None:
            self.node_type = context.active_node.type
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        node_type = self.node_type
        for node in get_active_node_tree(context).nodes:
            if node.type == node_type:
                node.use_custom_color = True
                node.color = self.node_color
                if self.select_nodes:
                    node.select = True

        return {"FINISHED"}
