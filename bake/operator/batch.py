import bpy
from bpy.types import Operator
from gorgious_utilities.uv.tool import smart_uv_project
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
            return
        props = context.active_object.GUProps.lod
        if not props.target_lods:
            return
        return True

    def execute(self, context):
        props = context.active_object.GUProps.lod
        props.is_running = False
        obj_hp = context.active_object
        for i, lod in enumerate(props.target_lods):
            obj_lp = lod.object
            if obj_lp is None:
                continue
            smart_uv_project(
                obj_lp,
                angle_limit=0.959931,
                island_margin=0.001,
            )
            bsdf_mat_lp = BSDFMaterial(name=obj_lp.name)
            set_material_slot_to_material(obj_lp, bsdf_mat_lp.material)

            gorgious_utilities.bake.tool.update_settings(
                context.scene,
                use_selected_to_active=True,
                cage_extrusion=0.04,
            )

            bsdf_mat_hp = BSDFMaterial(name="HP BSDF Material", material=obj_hp.data.materials[0])

            # bsdf_mat_lp.define_bake(bsdf_mat_hp, obj_lp, obj_hp)
            bsdf_mat_lp.bake_all_maps(bsdf_mat_hp, obj_lp, obj_hp, props.pixel_size)
            # bsdf_mat_lp.bake_from_normal(props.pixel_size)
            # bsdf_mat_lp.bake_from_albedo(props.pixel_size)

            # obj_lp.location = (obj_hp.dimensions[0] * 1.1 * (i + 1), 0, 0)

        return {"FINISHED"}
