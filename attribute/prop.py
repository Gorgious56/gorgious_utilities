import bpy

from bpy.props import (
    PointerProperty,
    FloatProperty,
    FloatVectorProperty,
    StringProperty,
    IntProperty,
    BoolProperty,
)
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject


def update_attribute_ui(self, context):
    if not context.active_object:
        return
    bpy.ops.gu.attribute_set(
        mode=context.scene.tool_settings.mesh_select_mode,
        attribute_name=context.active_object.data.attributes.active.name,
    )


class AttributeProps(PropertyGroup):
    FLOAT: FloatProperty(update=update_attribute_ui)
    INT: IntProperty(update=update_attribute_ui)
    FLOAT2: FloatVectorProperty(update=update_attribute_ui, size=2)
    STRING: StringProperty(
        update=update_attribute_ui,
    )
    FLOAT_VECTOR: FloatVectorProperty(update=update_attribute_ui, size=3)
    FLOAT_COLOR: FloatVectorProperty(
        update=update_attribute_ui, size=4, subtype="COLOR", min=0, max=1, default=(0, 0, 0, 1)
    )
    BOOLEAN: BoolProperty(update=update_attribute_ui)
    INT8: IntProperty(update=update_attribute_ui)


GUPropsObject.__annotations__["attribute"] = PointerProperty(type=AttributeProps)
