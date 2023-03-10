import functools
from bpy.types import Operator
import bpy.app.timers


def run_remesh(source_object):
    scene = bpy.context.scene
    props = source_object.GUProps.lod
    if props.is_running:
        current_lod = next(lod for lod in props.target_lods if not lod.object)
        obj_lp = bpy.data.objects.get("Retopo_" + source_object.name)
        if obj_lp is None:
            return 0.2
        tris = len(obj_lp.data.polygons) * 2
        if tris > 1.1 * current_lod.target_tris:
            new_value = scene.qremesher.target_count * min(0.9, current_lod.target_tris / tris)
            print(f"{tris} > {current_lod.target_tris}, remeshing at lower value {new_value}")
            mesh_name = obj_lp.data.name
            bpy.data.objects.remove(obj_lp)
            bpy.data.meshes.remove(bpy.data.meshes[mesh_name])
            scene.qremesher.target_count = int(new_value)

            with bpy.context.temp_override(active_object=source_object, selected_objects=[source_object]):
                bpy.ops.qremesher.remesh()
            return 0.2
        current_lod.object = obj_lp
        obj_lp.select_set(False)
        obj_lp.name = source_object.name + "_LP_" + str(round(tris / 1000, 0 if tris >= 100000 else 1)) + "k"
        props.is_running = False
        return 0.2
    else:
        with bpy.context.temp_override(active_object=source_object, selected_objects=[source_object]):
            for lod in props.target_lods:
                if lod.object is not None:
                    continue
                scene.qremesher.target_count = int(lod.target_tris / 2)
                props.is_running = True
                bpy.ops.qremesher.remesh()
                return 0.2
            props.reset_for_remesh()
            bpy.context.view_layer.objects.active = source_object
            source_object.select_set(True)
            if props.bake_after_remesh:
                print("bake !")
                return
                run_bake()
            return


class GU_OT_lod_remesh(Operator):
    bl_idname = "gu.lod_remesh"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        ao = context.active_object
        if not ao:
            return
        props = context.active_object.GUProps.lod
        if not props.target_lods:
            return
        if not any(lod for lod in props.target_lods if lod.object is None):
            return
        return True

    def execute(self, context):
        context.scene.qremesher.hide_input = False
        props = context.active_object.GUProps.lod
        props.is_running = False
        props.source_object = context.active_object
        bpy.app.timers.register(functools.partial(run_remesh, context.active_object))

        return {"FINISHED"}
