from bpy.types import PropertyGroup, Object, Scene
from bpy.props import PointerProperty, IntProperty


class StringPropertyGroup(PropertyGroup):
    pass


class IntPropertyGroup(PropertyGroup):
    value: IntProperty()


class ObjectPointerProperty(PropertyGroup):
    pointer: PointerProperty(type=Object, name="Target")


class GUPropsObject(PropertyGroup):
    pass


class GUPropsScene(PropertyGroup):
    pass


def register():
    Object.GUProps = PointerProperty(type=GUPropsObject)
    Scene.GUProps = PointerProperty(type=GUPropsScene)


def unregister():
    del Object.GUProps
