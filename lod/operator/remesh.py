import bpy
from bpy.types import Operator
from bpy.props import IntProperty, BoolProperty, StringProperty, FloatProperty


class GU_OT_lod_remesh(Operator):
    bl_idname = "gu.lod_remesh"
    bl_label = ""
    source_object_name: StringProperty()
    qremesh_origin_hide_input: BoolProperty()
    qremesh_origin_target_count: IntProperty()
    qremesh_origin_adaptive_size: FloatProperty(default=0.5, min=0, max=1)
    qremesh_origin_adapt_quad_count: BoolProperty(default=False)
    qremesh_origin_use_vertex_color: BoolProperty(default=True)
    qremesh_origin_use_materials: BoolProperty(default=False)
    qremesh_origin_use_normals: BoolProperty(default=False)
    qremesh_origin_autodetect_hard_edges: BoolProperty(default=True)
    last_tris: IntProperty()
    is_running: BoolProperty(default=False)

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
        for ann in self.__annotations__:
            if ann.startswith("qremesh_origin_"):
                origin_value = getattr(qremesher_props, ann.split("qremesh_origin_")[1])
                setattr(self, ann, origin_value)
        qremesher_props.hide_input = False

        self.is_running = False
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
        if self.is_running:
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
            obj_lp.select_set(False)
            if source_object.name[:-1].endswith("LOD"):
                obj_lp.name = f"{source_object.name[:-1]}{current_lod.number}"
            else:
                obj_lp.name = f"{source_object.name}_LOD{current_lod.number}"
            obj_lp.data.name = obj_lp.name
            self.is_running = False
            obj_lp.GUProps.lod.source_high_poly_props.object = source_object
            return {"RUNNING_MODAL"}
        else:
            with context.temp_override(active_object=source_object, selected_objects=[source_object]):
                for lod in props.target_lods:
                    if lod.object is not None:
                        continue
                    qremesher_props.target_count = int(lod.target_tris / 2)
                    self.is_running = True
                    lod_remesh_settings = source_object.GUProps.lod.remesher_settings
                    if not lod_remesh_settings.use_defaults:
                        for ann in lod_remesh_settings.__annotations__:
                            setattr(qremesher_props, ann, getattr(lod_remesh_settings, ann))
                    bpy.ops.qremesher.remesh()
                    return {"RUNNING_MODAL"}
                self.is_running = False
                bpy.context.view_layer.objects.active = source_object
                source_object.select_set(True)
                if props.bake_after_remesh:
                    print("bake !")
                for ann in self.__annotations__:
                    if ann.startswith("qremesh_origin_"):
                        origin_value = getattr(self, ann)
                        setattr(qremesher_props, ann.split("qremesh_origin_")[1], origin_value)
                qremesher_props.target_count = self.qremesh_origin_target_count
                qremesher_props.hide_input = self.qremesh_origin_hide_input
                return {"FINISHED"}
