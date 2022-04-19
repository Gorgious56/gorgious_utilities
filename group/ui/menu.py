import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_group_ops(self, _):
    layout = self.layout
    layout.operator("group.by_custom_prop", text="Group by Custom Prop", icon="GROUP")
    layout.operator("group.copy_to_selected", text="Copy Group to Selected", icon="EYEDROPPER")
    layout.operator("group.display_by_custom_prop", text="Display by Custom Prop", icon="COLLECTION_COLOR_01")


class GU_Menu_Group(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_object_relations: draw_group_ops,
    }


def register():
    GU_Menu_Group.register()


def unregister():
    GU_Menu_Group.unregister()
