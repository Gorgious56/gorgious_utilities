import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, StringProperty
from gorgious_utilities.uv.tool import smart_uv_project


class GU_OT_lod_remesh(Operator):
    bl_idname = "gu.lod_remesh"
    bl_label = ""
    source_object_name: StringProperty()
    qremesh_origin_hide_input = BoolProperty()
    qremesh_origin_target_count = IntProperty()
    last_tris: IntProperty()

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

    def invoke(self, context, event):
        qremesher_props = context.scene.qremesher
        self.qremesh_origin_hide_input = qremesher_props.hide_input
        qremesher_props.hide_input = False
        self.qremesh_origin_target_count = qremesher_props.target_count

        props = context.active_object.GUProps.lod
        props.is_running = False
        self.source_object_name = context.active_object.name
        context.window_manager.modal_handler_add(self)
        return {"RUNNING_MODAL"}

    def modal(self, context, event):
        source_object = bpy.data.objects.get(self.source_object_name)
        if source_object is None:
            return {"CANCELED"}
        props = source_object.GUProps.lod
        scene = context.scene
        qremesher_props = scene.qremesher
        if props.is_running:
            current_lod = next(lod for lod in props.target_lods if not lod.object)
            obj_lp = bpy.data.objects.get("Retopo_" + source_object.name)
            if obj_lp is None:
                return {"RUNNING_MODAL"}
            tris = len(obj_lp.data.polygons) * 2
            if tris != self.last_tris and tris > 1.2 * current_lod.target_tris:
                qremesher_tris = qremesher_props.target_count * 2
                new_value = qremesher_tris * current_lod.target_tris / tris
                print(f"{tris} > {current_lod.target_tris}, remeshing at lower value {new_value}")
                mesh_name = obj_lp.data.name
                bpy.data.objects.remove(obj_lp)
                bpy.data.meshes.remove(bpy.data.meshes[mesh_name])
                qremesher_props.target_count = int(new_value / 2)

                with context.temp_override(active_object=source_object, selected_objects=[source_object]):
                    bpy.ops.qremesher.remesh()
                self.last_tris = tris
                return {"RUNNING_MODAL"}
            self.last_tris = -1
            current_lod.object = obj_lp
            smart_uv_project(
                obj_lp,
                angle_limit=0.959931,
                island_margin=0.001,
            )
            obj_lp.select_set(False)
            obj_lp.name = source_object.name + "_LP_" + str(round(tris / 1000, 0 if tris >= 100000 else 1)) + "k"
            props.is_running = False
            return {"RUNNING_MODAL"}
        else:
            with context.temp_override(active_object=source_object, selected_objects=[source_object]):
                for lod in props.target_lods:
                    if lod.object is not None:
                        continue
                    qremesher_props.target_count = int(lod.target_tris / 2)
                    props.is_running = True
                    bpy.ops.qremesher.remesh()
                    return {"RUNNING_MODAL"}
                props.reset_for_remesh()
                bpy.context.view_layer.objects.active = source_object
                source_object.select_set(True)
                if props.bake_after_remesh:
                    print("bake !")
                qremesher_props.target_count = self.qremesh_origin_target_count
                qremesher_props.hide_input = self.qremesh_origin_hide_input
                return {"FINISHED"}
