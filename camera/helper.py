import bpy


def reset_camera_rotation(context):
    camera = context.scene.camera
    if camera:
        camera.rotation_euler[1] = 0


def reset_camera_view(context):
    if context.space_data.region_3d.view_perspective != "CAMERA":
        bpy.ops.view3d.view_camera()
