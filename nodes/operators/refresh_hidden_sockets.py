import bpy
from gorgious_utilities.nodes.operators.helper import NodeTreeOperator, get_active_node_tree


class GU_OT_nodes_refresh_hidden_sockets(bpy.types.Operator, NodeTreeOperator):
    bl_idname = "nodes.refresh_hidden_sockets"
    bl_label = "Refresh Hidden Sockets"

    def execute(self, context):
        nodes = get_active_node_tree(context).nodes
        previously_selected_nodes = context.selected_nodes
        for node in previously_selected_nodes:
            node.select = False
        for node in nodes:
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
