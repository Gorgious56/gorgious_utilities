import bpy

from bpy.props import (
    PointerProperty,
    FloatProperty,
    FloatVectorProperty,
    StringProperty,
    IntProperty,
)
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject


class AttributeProps(PropertyGroup):
    FLOAT: FloatProperty()
    INT: IntProperty()
    FLOAT2: FloatVectorProperty(size=2)
    STRING: StringProperty()
    FLOAT_VECTOR: FloatVectorProperty(size=3)
    FLOAT_COLOR: FloatVectorProperty(size=4, subtype="COLOR", min=0, max=1, default=(0, 0, 0, 1))


GUPropsObject.__annotations__["attribute"] = PointerProperty(type=AttributeProps)
