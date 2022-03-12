import bpy


class GU_PT_node_editor_qol(bpy.types.Panel):
    bl_space_type = "NODE_EDITOR"
    bl_label = "QOL"
    bl_region_type = "UI"
    bl_category = "Tool"

    def draw(self, context):
        self.layout.operator("nodes.color_by_type")
