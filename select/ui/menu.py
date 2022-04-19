import bpy
from gorgious_utilities.core.menu import GU_Menu


def draw_select_used_booleans(self, context):
    self.layout.operator("select.used_booleans")


def draw_select_by_property(self, context):
    self.layout.operator("select.by_property")


class GU_Menu_Select(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_select_object: draw_select_used_booleans,
        bpy.types.VIEW3D_MT_select_object: draw_select_by_property,
    }


def register():
    GU_Menu_Select.register()


def unregister():
    GU_Menu_Select.unregister()
