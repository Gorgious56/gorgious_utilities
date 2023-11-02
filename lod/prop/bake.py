from bpy.props import CollectionProperty, BoolProperty, FloatProperty

from bpy.types import PropertyGroup
from gorgious_utilities.core.property.tool import display_name
from gorgious_utilities.lod.prop.texture import TextureSetting


class BakeSettings(PropertyGroup):
    cage_extrusion: FloatProperty(min=0, name="Cage Extrusion", default=0.04)
    texture_settings: CollectionProperty(type=TextureSetting)
    baked: BoolProperty(name="Baked")
    reset_origin_on_bake: BoolProperty(default=True)

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
        layout.prop(self, "baked", text="Baked ?", icon="TEXTURE")
        layout.prop(
            self, "reset_origin_on_bake", text=display_name(self, "reset_origin_on_bake"), icon="OBJECT_ORIGIN"
        )
        self.draw_texture_settings(layout)

    def draw_texture_settings(self, layout):
        obj = self.id_data
        if not obj or not obj.data or not obj.data.materials:
            return
        box = layout.box()
        row = box.row(align=True)
        mat = obj.data.materials[0]
        column = box.column(align=True)
        normal_input = False
        try:
            nodes = mat.node_tree.nodes
            bsdf = nodes["Principled BSDF"]
            for input in bsdf.inputs:
                if not input.links:
                    continue
                row = column.row(align=True)
                if input.name == "Normal":
                    normal_input = True
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
        if not normal_input:
            row = column.row(align=True)
            row.label(text="Normal")
            row.context_pointer_set("collection_property_holder", self)
            texture_setting, index = self.get_texture_setting_and_index_for_map("Normal")
            if texture_setting:
                if texture_setting.active:
                    texture_setting.draw(row, index)
                else:
                    row.prop(texture_setting, "active", icon="LINKED", text="")
            else:
                op_add = row.operator("gu.collection_property_operations", icon="LINKED", text="")
                op_add.collection_property_name = "texture_settings"
                op_add.operation = "ADD"
                op_add.item_name = "Normal"
