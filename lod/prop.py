from bpy.props import CollectionProperty, PointerProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
from bpy.types import PropertyGroup, Object
from gorgious_utilities.core.prop import GUPropsObject, ObjectPointerProperty


class LODPropertyGroup(PropertyGroup):
    target_tris: IntProperty(min=1, default=500, name="Tris")
    object: PointerProperty(type=Object, name="")
    remeshed: BoolProperty(name="Remeshed", options={"HIDDEN"}, default=False)

    def draw(self, layout):
        if not self.object:
            layout.prop(self, "target_tris")
        layout.prop(self, "object")


class LodProps(PropertyGroup):
    target_lods: CollectionProperty(type=LODPropertyGroup)
    image_size: FloatProperty(name="Image Size", default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)

    is_running: BoolProperty(default=False)
    bake_after_remesh: BoolProperty(default=True)

    @property
    def pixel_size(self):
        return int(self.image_size * 1024)

    def reset_for_remesh(self):
        for lod in self.target_lods:
            lod.remeshed = False
        self.is_running = False


GUPropsObject.__annotations__["lod"] = PointerProperty(type=LodProps)
