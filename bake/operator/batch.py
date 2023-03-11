from bpy.types import Operator
from gorgious_utilities.material.tool import set_material_slot_to_material
from gorgious_utilities.material.bsdf import BSDFMaterial
import gorgious_utilities.bake.tool


class GU_OT_bake_batch(Operator):
    bl_idname = "gu.bake_batch"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        ao = context.active_object
        if not ao:
            return False
        props = context.active_object.GUProps.lod
        if not props.target_lods:
            return False
        if not any(lod.object for lod in props.target_lods):
            return False
        if not ao.data.materials:
            return False
        mat = ao.data.materials[0]
        if mat is None or not mat.use_nodes:
            return False

        return True

    def execute(self, context):
        props = context.active_object.GUProps.lod
        props.is_running = False
        obj_hp = context.active_object
        render_settings_origin = gorgious_utilities.bake.tool.store_settings(context.scene.render.bake)
        gorgious_utilities.bake.tool.update_settings(
            context.scene.render.bake,
            use_selected_to_active=True,
            cage_extrusion=0.04,
        )

        for lod in props.target_lods:
            obj_lp = lod.object
            if obj_lp is None:
                continue
            if lod.baked:
                continue
            obj_lp_origin = obj_lp.location
            if lod.reset_origin_on_bake:
                obj_lp_origin.location = (0, 0, 0)
            bsdf_mat_lp = BSDFMaterial(name=obj_lp.name)
            set_material_slot_to_material(obj_lp, bsdf_mat_lp.material)

            bsdf_mat_hp = BSDFMaterial(name="HP BSDF Material", material=obj_hp.data.materials[0])

            bsdf_mat_lp.bake_all_maps(bsdf_mat_hp, obj_lp, obj_hp, props.pixel_size)
            lod.baked = True
            if lod.reset_origin_on_bake:
                obj_lp_origin.location = obj_lp_origin

        context.view_layer.objects.active = lod.id_data
        lod.id_data.select_set(True)

        gorgious_utilities.bake.tool.update_settings(
            context.scene.render.bake,
            **render_settings_origin,
        )

        return {"FINISHED"}
