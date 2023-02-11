from bpy.props import CollectionProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject
from gorgious_utilities.gpu.tool import MeshDrawer


def update_draw_mesh_gpu(self, context):
    if MeshDrawer.installed:
        MeshDrawer.uninstall()
    MeshDrawer.install(context)


class GPUProps(PropertyGroup):
    draw_mesh_edit_mode: BoolProperty(default=False, update=update_draw_mesh_gpu, name="Draw XRAY")
    draw_mesh_object_mode: BoolProperty(default=False, update=update_draw_mesh_gpu, name="Draw XRAY")


GUPropsObject.__annotations__["gpu"] = PointerProperty(type=GPUProps)
