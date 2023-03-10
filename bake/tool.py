import bpy


def update_settings(scene, **kwargs):
    for k, v in kwargs.items():
        setattr(scene.render.bake, k, v)


def bake(source, target, type="EMIT"):
    with bpy.context.temp_override(active_object=target, selected_objects=[target, source]):
        bpy.ops.object.bake(type=type)
