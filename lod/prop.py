import bpy
from bpy.props import CollectionProperty, PointerProperty, StringProperty, BoolProperty, IntProperty, FloatProperty
from bpy.types import PropertyGroup, Object
from gorgious_utilities.core.prop import GUPropsObject

from gorgious_utilities.core.property.tool import display_name


class TextureSetting(PropertyGroup):
    name: StringProperty()
    image_size: FloatProperty(default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)
    use_alpha: BoolProperty(default=False)
    bake_me: BoolProperty(default=True)
    active: BoolProperty(default=True)

    @property
    def pixel_size(self):
        return int(self.image_size * 1024)

    def draw(self, layout, index=None):
        if self.bake_me:
            layout.prop(self, "image_size", text=display_name(self, "image_size"))
        layout.prop(self, "bake_me", text="", icon="TEXTURE")
        layout.prop(self, "use_alpha", text="", icon="IMAGE_RGB_ALPHA")
        layout.prop(self, "active", icon="UNLINKED", text="")


class BakeSettings(PropertyGroup):
    cage_extrusion: FloatProperty(min=0, name="Cage Extrusion", default=0.04)
    texture_settings: CollectionProperty(type=TextureSetting)

    def get_pixel_size_for_map(self, map_name):
        texture_setting, _ = self.get_texture_setting_and_index_for_map(map_name)
        if texture_setting and texture_setting.active:
            return texture_setting.pixel_size
        return self.pixel_size

    def get_texture_setting_and_index_for_map(self, map_name):
        for i, texture_setting in enumerate(self.texture_settings):
            if texture_setting.name == map_name:
                return texture_setting, i
        return None, -1

    def draw(self, layout):
        layout.prop(self, "cage_extrusion")
        self.draw_texture_settings(layout)

    def draw_texture_settings(self, layout):
        obj = self.id_data.GUProps.lod.source_high_poly_props.object
        if not obj or not obj.data or not obj.data.materials:
            return
        box = layout.box()
        row = box.row(align=True)
        mat = obj.data.materials[0]
        column = box.column(align=True)
        try:
            nodes = mat.node_tree.nodes
            bsdf = nodes["Principled BSDF"]
            for input in bsdf.inputs:
                if not input.links:
                    continue
                row = column.row(align=True)
                row.label(text=input.name)
                row.context_pointer_set("collection_property_holder", self)
                texture_setting, index = self.get_texture_setting_and_index_for_map(input.name)
                if texture_setting:
                    if texture_setting.active:
                        texture_setting.draw(row, index)
                    else:
                        row.prop(texture_setting, "active", icon="LINKED", text="")
                else:
                    op_add = row.operator("gu.collection_property_operations", icon="LINKED", text="")
                    op_add.collection_property_name = "texture_settings"
                    op_add.operation = "ADD"
                    op_add.item_name = input.name
        except (AttributeError, KeyError):
            pass


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

    def draw(self, layout):

        split = layout.split(factor=0.2, align=True)
        split.prop(self, "number", text="")
        if self.object:
            split.prop(self, "object")
            op = layout.operator("GU_OT_command", icon="RESTRICT_SELECT_OFF", text="")
            op.command = f'context.view_layer.objects.active.select_set(False); context.view_layer.objects.active = context.scene.objects["{self.object.name}"]; context.view_layer.objects.active.select_set(True);'

            layout.prop(self.object.GUProps.lod, "baked", icon="TEXTURE", text="")
            layout.context_pointer_set("lod", self)
            layout.popover("GU_PT_object_lod_settings", text="", icon="SETTINGS")
        else:
            split = split.split(factor=0.3, align=True)
            split.prop(self, "object")
            split.prop(self, "target_tris")

    def on_add(self):
        index = int(repr(self).rsplit("[", 1)[1].split("]")[0])
        self.number = index


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
        layout.prop(self, "object")


class LodProps(PropertyGroup):
    target_lods: CollectionProperty(type=LODPropertyGroup)
    source_high_poly_props: PointerProperty(type=HighPolyProps)
    image_size_default: FloatProperty(default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)
    source_object: PointerProperty(type=Object)
    remesher_settings: PointerProperty(type=RemesherSettings)

    bake_after_remesh: BoolProperty(default=True)

    baked: BoolProperty(name="Baked")
    reset_origin_on_bake: BoolProperty(default=True)
    bake_settings: PointerProperty(type=BakeSettings)

    @property
    def pixel_size(self):
        return int(self.image_size_default * 1024)

    def draw(self, layout):
        if self.target_lods:
            self.draw_texture_settings(layout)
            self.remesher_settings.draw(layout)
        else:
            self.draw_lod_settings(layout)

    def draw_lod_settings(self, layout):
        box = layout.box()
        box.label(text="LOD Settings")
        self.source_high_poly_props.draw(box)
        box.prop(self, "baked", text=display_name(self, "baked"), icon="TEXTURE")
        box.prop(self, "reset_origin_on_bake", text=display_name(self, "reset_origin_on_bake"), icon="OBJECT_ORIGIN")
        # TODO add button to bake only me
        self.bake_settings.draw(box)

    def draw_texture_settings(self, layout):
        layout.prop(self, "image_size_default", text=display_name(self, "image_size_default"))


GUPropsObject.__annotations__["lod"] = PointerProperty(type=LodProps)
