import bpy
from bpy.props import CollectionProperty, PointerProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
from bpy.types import PropertyGroup, Object
from gorgious_utilities.core.prop import GUPropsObject

import gorgious_utilities.core.property.collection.ui.draw_generic
from gorgious_utilities.core.property.tool import display_name

from gorgious_utilities.lod.prop.bake import BakeSettings
from gorgious_utilities.lod.prop.remesh import RemesherSettings


def update_lod_object(self, context):
    obj_lp = self.object
    if obj_lp:
        self.object_cache = self.object
        obj_lp_props = obj_lp.GUProps.lod
        obj_lp_props.source_high_poly_props.object = context.active_object
    else:
        if not self.object_cache:
            return
        obj_lp_props = self.object_cache.GUProps.lod
        obj_lp_props.source_high_poly_props.object = None
        self.object_cache = None


class LODPropertyGroup(PropertyGroup):
    target_tris: IntProperty(min=1, default=500, name="Tris")
    object: PointerProperty(
        type=Object,
        name="",
        poll=lambda s, o: o.type == "MESH" and o != bpy.context.active_object,
        update=update_lod_object,
    )
    object_cache: PointerProperty(type=Object)
    number: IntProperty(default=0, min=0, name="LOD")

    bake_settings: PointerProperty(type=BakeSettings)

    def draw(self, layout):

        split = layout.split(factor=0.2, align=True)
        split.prop(self, "number", text="")
        if self.object:
            split.prop(self, "object")
            op = layout.operator("gu.select_and_set_active", icon="RESTRICT_SELECT_OFF", text="")
            op.object_name = self.object.name

            layout.prop(self.object.GUProps.lod.get_lod_settings().bake_settings, "baked", icon="TEXTURE", text="")
            layout.context_pointer_set("lod", self)
            layout.popover("GU_PT_object_lod_settings", text="", icon="SETTINGS")
        else:
            split = split.split(factor=0.3, align=True)
            split.prop(self, "object")
            split.prop(self, "target_tris")

    def on_add(self):
        index = int(repr(self).rsplit("[", 1)[1].split("]")[0])
        self.number = index


def update_source_obj_high_poly(self, context):
    obj_hp = self.object
    if obj_hp:
        self.object_cache = self.object
        obj_hp_props = obj_hp.GUProps.lod
        for lod in obj_hp_props.target_lods:
            if lod.object == self.id_data:
                return
            if lod.object is None:
                lod.object = self.id_data
                return
        new = obj_hp_props.target_lods.add()
        new.on_add()
        new.object = self.id_data
    else:
        if not self.object_cache:
            return
        obj_hp_props = self.object_cache.GUProps.lod
        for lod in obj_hp_props.target_lods:
            if lod.object == self.id_data:
                lod.object = None
                break
        self.object_cache = None


class HighPolyProps(PropertyGroup):
    object: PointerProperty(type=Object, update=update_source_obj_high_poly, name="High Poly Source Object")
    object_cache: PointerProperty(type=Object)

    def draw(self, layout):
        if not self.object:
            return
        row = layout.row(align=True)
        row.prop(self, "object")
        op = row.operator("gu.select_and_set_active", text="", icon="RESTRICT_SELECT_OFF")
        op.object_name = self.object.name

    def clear(self):
        self.object = None
        self.object_cache = None


class LodProps(PropertyGroup):
    target_lods: CollectionProperty(type=LODPropertyGroup)
    source_high_poly_props: PointerProperty(type=HighPolyProps)
    image_size_default: FloatProperty(default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)
    remesher_settings: PointerProperty(type=RemesherSettings)

    @property
    def pixel_size(self):
        return int(self.image_size_default * 1024)

    def draw(self, layout):
        if self.target_lods or not self.source_high_poly_props.object:
            box = layout.box()
            box.label(text="LODs")
            row = box.row(align=True)
            row.operator("gu.lod_remesh", text="Create LODs", icon="MOD_REMESH")
            row.operator("gu.bake_batch", text="Bake LODs", icon="TEXTURE")
            row.operator("gu.bake_sanitize", text="", icon="GREASEPENCIL")
            gorgious_utilities.core.property.collection.ui.draw_generic.draw(box, self.target_lods)
            self.draw_texture_settings(layout)
            self.remesher_settings.draw(layout)
        else:
            self.draw_lod_settings(layout)

    def draw_lod_settings(self, layout):
        box = layout.box()
        box.label(text="LOD Settings")
        self.source_high_poly_props.draw(box)
        row = box.row(align=True)
        row.operator("gu.bake_batch", icon="SCENE", text="Bake Me !")
        if lod_settings := self.get_lod_settings():
            lod_settings.bake_settings.draw(box)

    def draw_texture_settings(self, layout):
        layout.prop(self, "image_size_default", text=display_name(self, "image_size_default"))

    def clear(self):
        self.target_lods.clear()
        self.source_high_poly_props.clear()

    def get_lod_settings(self):
        source = self.source_high_poly_props.object
        if source:
            for lod in source.GUProps.lod.target_lods:
                if lod.object == self.id_data:
                    return lod
        return None


GUPropsObject.__annotations__["lod"] = PointerProperty(type=LodProps)
