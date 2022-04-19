import bpy
from gorgious_utilities.core.menu import GU_Menu


def draw_hatches(self, _):
    layout = self.layout
    layout.operator("gpencil.generate_hatches", icon="TEXTURE_DATA")


class GU_Menu_GP(GU_Menu):
    appends = {
        bpy.types.GPENCIL_MT_material_context_menu: draw_hatches,
    }


def register():
    GU_Menu_GP.register()


def unregister():
    GU_Menu_GP.unregister()
