import bpy
from bpy.types import Panel


class GU_PT_image_node_editor_node(Panel):
    bl_space_type = "NODE_EDITOR"
    bl_label = "Tool"
    bl_category = "Node"
    bl_region_type = "UI"

    @classmethod
    def poll(cls, context):
        if len(context.selected_nodes) != 2:
            return False
        for node in context.selected_nodes:
            if not isinstance(node, bpy.types.ShaderNodeTexImage):
                return False
        return True

    def draw(self, context):
        layout = self.layout
        layout.context_pointer_set(
            "source_image", next(n.image for n in context.selected_nodes if n != context.active_node)
        )
        layout.context_pointer_set("target_image", context.active_node.image)
        op = layout.operator("gu.image_transfer_value_to_alpha")
