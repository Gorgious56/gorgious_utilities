import bpy


class GU_PT_node_editor_qol(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_label = "QOL"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        layout = self.layout
        layout.operator("nodes.color_by_type", icon="COLORSET_02_VEC")

        row = layout.row(align=True)
        active_node = context.active_node
        if active_node is not None:
            row.operator_context = "EXEC_DEFAULT"
        op = row.operator("gu.nodes_select_by_type", icon="RESTRICT_SELECT_OFF")
        if active_node is not None:
            op.node_type = active_node.type
            row.operator_context = "INVOKE_DEFAULT"
        row.operator("gu.nodes_select_by_type", text="", icon="VIEWZOOM")

        layout.operator("nodes.refresh_hidden_sockets", icon="HIDE_ON")
        layout.operator("nodes.create_factor_input", icon="ADD")

        layout.label(text=f"Class : {context.active_node.__class__.__name__}")
