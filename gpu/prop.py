from bpy.props import CollectionProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject
from gorgious_utilities.gpu.tool import MeshDrawer


def update_draw_mesh_gpu(self, context):
    if not MeshDrawer.installed:
        MeshDrawer.install(context)


class GPUProps(PropertyGroup):
    draw_mesh: BoolProperty(default=False, update=update_draw_mesh_gpu)


GUPropsObject.__annotations__["gpu"] = PointerProperty(type=GPUProps)
