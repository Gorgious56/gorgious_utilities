import bpy
from bpy.types import Operator
from gorgious_utilities.material.bsdf import BSDFMaterial


class GU_OT_bake_sanitize(Operator):
    bl_idname = "gu.bake_sanitize"
    bl_label = ""

    def execute(self, context):
        mats = [context.active_object.data.materials[0]]
        for lod in context.active_object.GUProps.lod.target_lods:
            obj = lod.object
            if not obj or not obj.data or not obj.data.materials:
                continue
            mat = obj.data.materials[0]
            mat.name = obj.name
            obj.data.name = obj.name
            mats.append(mat)
        for mat in mats:
            bsdf_mat = BSDFMaterial(mat.name, mat)
            for input_name, texture_node in bsdf_mat.get_texture_maps().items():
                if input_name == "Alpha":
                    continue
                if not hasattr(texture_node, "image"):
                    continue
                texture_node.image.name = mat.name + "_" + input_name

        for obj in bpy.data.objects:
            if obj.name in context.scene.objects:
                continue
            bpy.data.objects.remove(obj)
        return {"FINISHED"}
