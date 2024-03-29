import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_modifiers_properties(self, context):
    layout = self.layout
    row = layout.row(align=True)
    row.operator("modifier.replace_gn_a_with_gn_b", icon="NODETREE")
    row.operator("modifier.replace_output_name", icon="GROUP_VCOL")
    row.operator("gu.select_same_gn", icon="RESTRICT_SELECT_OFF")

    row = layout.row(align=True)
    sub_row = row.row(align=True)
    sub_row.operator("gu.select_used_objects", icon="LINKED", text="Select Used Objects")
    sub_row.operator("gu.select_where_i_am_used", icon="LINKED", text="Select Objects Using Me")
    # op = sub_row.operator("object.make_links_data", text="Copy", icon="PASTEDOWN")
    # op.type = "MODIFIERS"
    # sub_row.operator("modifier.drive", icon="DECORATE_DRIVER")
    # sub_row.operator("modifier.sync", text="Synch", icon="UV_SYNC_SELECT")
    # sub_row.enabled = bool(len(context.view_layer.objects.selected) > 1 and context.active_object)
    # row.operator("modifier.desync", text="Desynch", icon="UNLINKED")


class GU_Menu_Modifier(GU_Menu):
    prepends = {
        bpy.types.DATA_PT_modifiers: draw_modifiers_properties,
    }


def register():
    GU_Menu_Modifier.register()


def unregister():
    GU_Menu_Modifier.unregister()
