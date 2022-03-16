import bpy
from gorgious_utilities.nodes.operators.helper import NodeTreeOperator, get_active_node_tree


class GU_OT_nodes_Hidden(bpy.types.Operator, NodeTreeOperator):
    bl_idname = "nodes.create_factor_input"
    bl_label = "Create Factor Input"

    default_value: bpy.props.FloatProperty(name="Default Value", min=0, max=1)
    name: bpy.props.StringProperty(name="Name")

    @classmethod
    def poll(cls, context):
        active_node_tree = get_active_node_tree(context)
        if active_node_tree is None:
            return False
        return isinstance(active_node_tree, (bpy.types.GeometryNodeTree, bpy.types.ShaderNodeTree))

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        tree = get_active_node_tree(context)
        nodes = tree.nodes
        input = next((n for n in nodes if n.type == "GROUP_INPUT"), None)
        if input is None:
            return {"FINISHED"}
        mix_type = {
            bpy.types.GeometryNodeTree: "ShaderNodeMixRGB",
            bpy.types.ShaderNodeTree: "ShaderNodeMixRGB",
        }.get(type(tree), None)
        if mix_type is None:
            print("Node tree not supported for factor input")
            return {"FINISHED"}
        new_mix = nodes.new(mix_type)
        new_mix.inputs[0].default_value = self.default_value
        tree.links.new(input.outputs[-1], new_mix.inputs[0])
        input.outputs[-2].name = self.name or "Fac"
        nodes.remove(new_mix)
        return {"FINISHED"}
