from bpy.types import Operator
from gorgious_utilities.material.tool import set_material_slot_to_material
from gorgious_utilities.material.bsdf import BSDFMaterial
import gorgious_utilities.bake.tool
from gorgious_utilities.uv.tool import smart_uv_project


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
        obj_hp = context.active_object
        render_settings_origin = gorgious_utilities.bake.tool.store_settings(context.scene.render.bake)

        for lod in props.target_lods:
            obj_lp = lod.object
            if obj_lp is None:
                continue
            obj_lp_props = obj_lp.GUProps.lod
            if obj_lp_props.baked:
                continue
            if not obj_lp.data.uv_layers:
                smart_uv_project(
                    obj_lp,
                    angle_limit=0.959931,
                    island_margin=0.001,
                )
            gorgious_utilities.bake.tool.update_settings(
                context.scene.render.bake,
                use_selected_to_active=True,
                cage_extrusion=obj_lp_props.bake_settings.cage_extrusion,
            )

            obj_lp_origin = obj_lp.location.copy()
            if obj_lp_props.reset_origin_on_bake and obj_lp_origin != (0, 0, 0):
                obj_lp.location = (0, 0, 0)

            material = None
            if obj_lp.data.materials:
                if obj_lp.data.materials[0] != obj_hp.data.materials[0]:
                    material = obj_lp.data.materials[0]
            bsdf_mat_lp = BSDFMaterial(name=obj_lp.name, material=material)
            set_material_slot_to_material(obj_lp, bsdf_mat_lp.material)

            bsdf_mat_hp = BSDFMaterial(name="HP BSDF Material", material=obj_hp.data.materials[0])

            bsdf_mat_lp.bake_all_maps(bsdf_mat_hp, obj_lp, obj_hp, props)
            obj_lp_props.baked = True
            if obj_lp_props.reset_origin_on_bake and obj_lp_origin != (0, 0, 0):
                obj_lp.location = obj_lp_origin

        context.view_layer.objects.active = lod.id_data
        lod.id_data.select_set(True)

        gorgious_utilities.bake.tool.update_settings(
            context.scene.render.bake,
            **render_settings_origin,
        )

        return {"FINISHED"}
