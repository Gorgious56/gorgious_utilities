import bpy
from gorgious_utilities.core.menu import GU_Menu


def draw_custom_properties_ops(self, _):
    row = self.layout.row(align=True)
    row.operator("property.copy_all", text="", icon="PROPERTIES")
    row.operator("property.copy_single", text="", icon="EYEDROPPER")
    row.operator("material.init_custom_properties", text="", icon="MATERIAL").overwrite = False
    row.operator("material.init_custom_properties", text="", icon="NODE_MATERIAL").overwrite = True
    row.operator("object.remove_all_custom_props", text="", icon="TRASH")


def draw_custom_props_links(self, _):
    layout = self.layout

    layout.operator("property.copy_all", text="Copy ALL Custom Properties")

    oc = layout.operator_context
    layout.operator_context = "INVOKE_DEFAULT"
    layout.operator("property.copy_single", text="Copy ONE Custom Property")
    layout.operator_context = oc

    layout.operator("property.copy_any", text="Copy ANY Internal Property")


class GU_Menu_CustomProperty(GU_Menu):
    appends = {
        bpy.types.OBJECT_PT_custom_props: draw_custom_properties_ops,
        bpy.types.VIEW3D_MT_make_links: draw_custom_props_links,
    }


def register():
    GU_Menu_CustomProperty.register()


def unregister():
    GU_Menu_CustomProperty.unregister()
