from bpy.props import CollectionProperty, PointerProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
from bpy.types import PropertyGroup, Object
from gorgious_utilities.core.prop import GUPropsObject, ObjectPointerProperty


class LODPropertyGroup(PropertyGroup):
    target_tris: IntProperty(min=1, default=500, name="Tris")
    object: PointerProperty(type=Object, name="", poll=lambda s, o: o.type == "MESH")
    remeshed: BoolProperty(name="Remeshed", default=False)
    baked: BoolProperty(name="Baked")
    reset_origin_on_bake: BoolProperty(default=True)

    def draw(self, layout):
        if not self.object:
            split = layout.split(factor=0.5)
            split.prop(self, "object")
            split.prop(self, "target_tris")
        else:
            split = layout.split(factor=0.8)
            split.prop(self, "object")
            split.label(text=f"{round(len(self.object.data.polygons) * 2 / 1000, 1)}k")

        layout.prop(self, "reset_origin_on_bake", icon="OBJECT_ORIGIN", text="")
        layout.prop(self, "baked", icon="TEXTURE", text="")
        layout.prop(self, "remeshed", icon="MOD_REMESH", text="")


class LodProps(PropertyGroup):
    target_lods: CollectionProperty(type=LODPropertyGroup)
    image_size: FloatProperty(name="Image Size", default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)
    source_object: PointerProperty(type=Object)
    cage_extrusion: FloatProperty(default=0.04)

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
