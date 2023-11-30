import bpy


class GU_OT_viewport_setup_overlays(bpy.types.Operator):
    bl_idname = "gu.viewport_setup_overlays"
    bl_label = "Setup Overlays"

    def execute(self, context):
        view_3d_area = next(
            (a for a in context.screen.areas if a.type == "VIEW_3D"), None
        )
        if view_3d_area is None:
            return {"CANCELLED"}
        shading = view_3d_area.spaces.active.shading
        shading.light = "FLAT"
        shading.color_type = "RANDOM"
        shading.show_xray = True
        shading.xray_alpha = 1
        shading.show_shadows = False
        shading.show_cavity = True
        shading.cavity_type = "BOTH"
        shading.cavity_ridge_factor = 1.5
        shading.cavity_valley_factor = 1.5

        return {"FINISHED"}
