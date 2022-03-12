from xml.dom.minicompat import NodeList
import bpy
from gorgious_utilities.nodes.helper import get_active_node_tree


class GU_OT_nodes_refresh_hidden_sockets(bpy.types.Operator):
    bl_idname = "nodes.refresh_hidden_sockets"
    bl_label = "Refresh Hidden Sockets"
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        return get_active_node_tree(context) is not None

    def execute(self, context):
        nodes = get_active_node_tree(context).nodes
        previously_selected_nodes = context.selected_nodes
        for node in nodes:
            node.select = False
            inputs_outputs = list(node.inputs) + list(node.outputs)
            for io in inputs_outputs:
                if io.hide:
                    node.select = True
                    break
        for _ in range(2):
            bpy.ops.node.hide_socket_toggle()

        for node in nodes:
            node.select = node in previously_selected_nodes
        return {"FINISHED"}
