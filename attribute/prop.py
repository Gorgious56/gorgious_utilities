import numpy as np

import bpy
import bmesh

from bpy.props import (
    PointerProperty,
    FloatProperty,
    FloatVectorProperty,
    StringProperty,
    IntProperty,
    IntVectorProperty,
    BoolProperty,
)
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject

from gorgious_utilities.attribute.tool import (
    get_bmesh_domain,
    get_layer_type,
)


def set_attribute_ui(self, value, attribute=None):
    obj = getattr(self, "id_data", bpy.context.active_object)
    bm = bmesh.from_edit_mesh(obj.data)

    attribute = attribute or self.active_attribute
    attribute_name = attribute.name
    domain = getattr(bm, get_bmesh_domain(attribute.domain))
    layer_type = getattr(domain.layers, get_layer_type(attribute.data_type))
    layer = layer_type.get(attribute_name)

    if isinstance(value, str):  # Strings are stored as byte strings.
        value = value.encode("utf-8")
    for item in domain:
        if item.select:
            item[layer] = value

    bmesh.update_edit_mesh(obj.data)


DEFAULT_VALUES = {"FLOAT": 0}


def get_attribute_ui(self):
    obj = self.id_data

    bm = bmesh.from_edit_mesh(obj.data)
    active_item = bm.select_history.active
    if active_item is None:
        mesh_select_mode = bpy.context.scene.tool_settings.mesh_select_mode
        # https://blender.stackexchange.com/a/233823/86891
        if mesh_select_mode[0]:
            container = bm.verts
        elif mesh_select_mode[1]:
            container = bm.edges
        elif mesh_select_mode[2]:
            container = bm.faces
        container_np = np.array(container)
        selected_np = np.frompyfunc(lambda a: a.select, 1, 1)
        selected_items = container_np[selected_np(container_np).astype(bool)]
        active_item = selected_items[0] if len(selected_items) > 0 else None
    if not active_item:
        return self.default_value()

    attribute = self.active_attribute
    attribute_name = attribute.name

    domain = getattr(bm, get_bmesh_domain(attribute.domain))
    layer_type = getattr(domain.layers, get_layer_type(attribute.data_type))
    layer = layer_type.get(attribute_name)

    if attribute.data_type == "STRING":
        return active_item[layer].decode("utf-8")  # Strings are stored as byte strings.
    return active_item[layer]


def get_attribute_index(self):
    mesh_select_mode = bpy.context.scene.tool_settings.mesh_select_mode
    for i in range(3):
        if mesh_select_mode[i]:
            return self.active_attribute_index_internal[i]


def set_attribute_index(self, value):
    mesh_select_mode = bpy.context.scene.tool_settings.mesh_select_mode
    for i in range(3):
        if mesh_select_mode[i]:
            self.active_attribute_index_internal[i] = value


class AttributeProps(PropertyGroup):
    FLOAT: FloatProperty(get=get_attribute_ui, set=set_attribute_ui)
    BOOLEAN: BoolProperty(get=get_attribute_ui, set=set_attribute_ui)
    INT: IntProperty(get=get_attribute_ui, set=set_attribute_ui)
    STRING: StringProperty(
        get=get_attribute_ui,
        set=set_attribute_ui,
    )
    FLOAT_VECTOR: FloatVectorProperty(get=get_attribute_ui, set=set_attribute_ui, size=3)
    FLOAT_COLOR: FloatVectorProperty(
        get=get_attribute_ui,
        set=set_attribute_ui,
        size=4,
        subtype="COLOR",
        min=0,
        soft_max=1,
        default=(0, 0, 0, 1),
    )

    FLOAT_copy: FloatProperty()
    INT_copy: IntProperty()
    STRING_copy: StringProperty()
    FLOAT_VECTOR_copy: FloatVectorProperty(size=3)
    FLOAT_COLOR_copy: FloatVectorProperty(size=4, subtype="COLOR", min=0, soft_max=1, default=(0, 0, 0, 1))

    active_attribute_index_internal: IntVectorProperty(size=3)
    active_attribute_index: IntProperty(get=get_attribute_index, set=set_attribute_index)

    @property
    def active_attribute(self):
        return (
            self.id_data.data.attributes[self.active_attribute_index]
            if self.active_attribute_index < len(self.id_data.data.attributes)
            else 0
        )

    def default_value(self):
        obj = self.id_data
        data_type = obj.data.attributes.active.data_type
        prop = self.bl_rna.properties[data_type]
        return prop.default_array if prop.is_array else prop.default


GUPropsObject.__annotations__["attribute"] = PointerProperty(type=AttributeProps)
