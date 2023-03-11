import bpy


def update_settings(bake_settings, **kwargs):
    for k, v in kwargs.items():
        setattr(bake_settings, k, v)


def store_settings(bake_settings):
    return {
        "use_selected_to_active": bake_settings.use_selected_to_active,
        "cage_extrusion": bake_settings.cage_extrusion,
    }


def bake(source, target, type="EMIT"):
    with bpy.context.temp_override(active_object=target, selected_objects=[target, source]):
        bpy.ops.object.bake(type=type)
