from bpy.types import PropertyGroup, Object
from bpy.props import PointerProperty


class StrProperty(PropertyGroup):
    pass


class GUPropsObject(PropertyGroup):
    pass


def register():
    Object.GUProps = PointerProperty(type=GUPropsObject)


def unregister():
    del Object.GUProps
