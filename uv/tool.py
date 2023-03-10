import bpy


def smart_uv_project(obj, angle_limit=None, island_margin=None):
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action="SELECT")

    params = {}
    if angle_limit is not None:
        params["angle_limit"] = angle_limit
    if island_margin is not None:
        params["island_margin"] = island_margin
    bpy.ops.uv.smart_project(**params)

    bpy.ops.object.editmode_toggle()
