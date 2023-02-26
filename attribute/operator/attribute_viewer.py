import bpy
from mathutils import Vector


def create_node(nodes, _type):
    return nodes.new(_type.__name__)


node_group_name = ".GU_ATTRIBUTE_VIEWER"


def get_or_create_viewer_node_tree():
    node_group = bpy.data.node_groups.get(node_group_name)
    if node_group is None:
        node_group = bpy.data.node_groups.new(name=node_group_name, type="GeometryNodeTree")
        nodes = node_group.nodes
        nodes.clear()
        input = create_node(nodes, bpy.types.NodeGroupInput)
        output = create_node(nodes, bpy.types.NodeGroupOutput)
        viewer = create_node(nodes, bpy.types.GeometryNodeViewer)
        viewer.data_type = "FLOAT_COLOR"
        attribute_input = create_node(nodes, bpy.types.GeometryNodeInputNamedAttribute)
        attribute_input.data_type = "FLOAT_COLOR"

        viewer.location = input.location + Vector((200, 0))
        output.location = input.location + Vector((200, 100))
        attribute_input.location = input.location - Vector((0, 100))
        node_group.inputs.clear()
        node_group.outputs.clear()

        links = node_group.links
        links.clear()
        links.new(attribute_input.outputs[2], viewer.inputs[3])
        links.new(input.outputs[0], viewer.inputs[0])
        links.new(input.outputs[0], output.inputs[0])
        links.new(input.outputs[1], attribute_input.inputs[0])
        """
        Attribute_Vector
        Attribute_Float
        Attribute_Color
        Attribute_Bool
        Attribute_Int
        """
    return node_group


class GU_OT_attribute_viewer(bpy.types.Operator):
    bl_idname = "gu.attribute_viewer"
    bl_label = "View Attribute"
    bl_options = {"UNDO"}
    attribute_name: bpy.props.StringProperty()
    update: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        node_group = get_or_create_viewer_node_tree()
        try:
            mod = next(m for m in context.active_object.modifiers if m.type == "NODES" and m.name == node_group_name)
            if self.update:
                mod[node_group.inputs[1].identifier] = self.attribute_name
                self.update = False
                context.active_object.data.update()
            else:
                context.active_object.modifiers.remove(mod)
            return {"FINISHED"}
        except StopIteration:
            mod = context.active_object.modifiers.new(type="NODES", name=node_group_name)
        mod.node_group = node_group
        mod[node_group.inputs[1].identifier] = self.attribute_name
        context.active_object.data.update()

        return {"FINISHED"}
