from bpy.props import CollectionProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup
from gorgious_utilities.core.prop import GUPropsObject


class ModifierInputState(PropertyGroup):
    show: BoolProperty(default=True)


class ModifierInputs(PropertyGroup):
    inputs: CollectionProperty(type=ModifierInputState)


class ModifierProps(PropertyGroup):
    modifier_inputs: CollectionProperty(type=ModifierInputs)


GUPropsObject.__annotations__["modifier"] = PointerProperty(type=ModifierProps)
