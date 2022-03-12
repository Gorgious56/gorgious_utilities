import bpy


class GU_PT_node_editor_qol(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_label = "QOL"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator("nodes.color_by_type")
        row = layout.row(align=True)
        row.operator("nodes.select_by_type")
        active_node = context.active_node
        if active_node is not None:
            print(active_node)
            row.operator_context = "EXEC_DEFAULT"
            op = row.operator("nodes.select_by_type", text="", icon="RESTRICT_SELECT_OFF")
            op.node_type = active_node.type
