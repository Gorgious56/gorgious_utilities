import bpy
from gorgious_utilities.core.ui.menu_factory import GU_Menu


def draw_custom_props_links(self, _):
    self.layout.operator("material.init_custom_properties", text="Copy Material Attributes")


def draw_update_viewport_material(self, _):
    self.layout.operator(
        "material.set_viewport_color_to_main_color", text="Update Viewport Color", icon="NODE_MATERIAL"
    )


class GU_Menu_Material(GU_Menu):
    appends = {
        bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
        bpy.types.MATERIAL_MT_context_menu: draw_update_viewport_material,
    }


def register():
    GU_Menu_Material.register()


def unregister():
    GU_Menu_Material.unregister()
