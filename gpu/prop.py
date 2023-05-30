from bpy.props import FloatVectorProperty, PointerProperty, BoolProperty, StringProperty, FloatProperty
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsScene
from gorgious_utilities.gpu.tool import MeshDrawer


def update_draw_mesh_gpu(self, context):
    if MeshDrawer.installed:
        MeshDrawer.uninstall()
    MeshDrawer.install(context)


class GPUPreferences(PropertyGroup):
    name: StringProperty(default="GPU Preferences")
    color_unselected: FloatVectorProperty(
        name="Unselected Vertex Color",
        size=4,
        subtype="COLOR",
        default=(0.7, 0.01, 0.45, 1),
        min=0,
        max=1,
    )

    def draw(self, layout):
        box = layout.box()
        box.label(text="GPU Preferences")
        column = box.column(align=True)
        column.row(align=True).prop(self, "color_unselected")


class GPUProps(PropertyGroup):
    draw_mesh: BoolProperty(default=False, update=update_draw_mesh_gpu, name="Draw XRAY")
    draw_mesh_attribute: BoolProperty(default=False, update=update_draw_mesh_gpu)


GUPropsScene.__annotations__["gpu"] = PointerProperty(type=GPUProps)
