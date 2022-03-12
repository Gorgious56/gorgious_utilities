from gorgious_utilities.nodes.helper import get_active_node_tree


class NodeTreeOperator:
    bl_options = {"UNDO", "REGISTER"}

    @classmethod
    def poll(cls, context):
        return get_active_node_tree(context) is not None
