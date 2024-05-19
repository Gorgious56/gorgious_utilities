import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


class GU_MT_modifier_ops(bpy.types.Menu):
    bl_idname = "GU_MT_modifier_ops"
    bl_label = "GU Ops"

    def draw(self, context):
        layout = self.layout
        layout.operator("modifier.replace_gn_a_with_gn_b", icon="NODETREE")
        layout.operator("modifier.replace_output_name", icon="GROUP_VCOL")
        layout.operator("gu.select_same_gn", icon="RESTRICT_SELECT_OFF")

        layout.operator("gu.select_used_objects", icon="LINKED", text="Select Used Objects")
        layout.operator("gu.select_where_i_am_used", icon="LINKED", text="Select Objects Using Me")


def draw_modifiers_properties(self, context):
    layout = self.layout

    layout.menu("GU_MT_modifier_ops")


class GU_Menu_Modifier(GU_Menu):
    prepends = {
        bpy.types.DATA_PT_modifiers: draw_modifiers_properties,
    }


def register():
    GU_Menu_Modifier.register()


def unregister():
    GU_Menu_Modifier.unregister()
