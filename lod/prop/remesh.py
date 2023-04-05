import bpy
from bpy.props import BoolProperty, IntProperty
from bpy.types import PropertyGroup

from gorgious_utilities.core.property.tool import display_name


class RemesherSettings(PropertyGroup):
    use_defaults: BoolProperty(default=True)
    adaptive_size: IntProperty(default=50, min=0, max=100, subtype="PERCENTAGE")
    adapt_quad_count: BoolProperty(default=True)
    use_vertex_color: BoolProperty(default=False)
    use_materials: BoolProperty(default=False)
    use_normals: BoolProperty(default=False, name="Use Normals Splitting")
    autodetect_hard_edges: BoolProperty(default=True)

    def draw(self, layout):
        box = layout.box()
        box.label(text="Remesher Settings")
        for ann in self.__annotations__:
            if ann == "use_defaults":
                box.prop(
                    self,
                    ann,
                    text=display_name(self, ann),
                    icon="LINKED" if self.use_defaults else "UNLINKED",
                )
            else:
                box.prop(self, ann, text=display_name(self, ann))
            if self.use_defaults:
                break
