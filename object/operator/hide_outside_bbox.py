import bpy
import mathutils


class GU_OT_clip_bbox(bpy.types.Operator):
    bl_idname = "object.clip_bbox"
    bl_label = "Clip Objects"
    bl_options = {"UNDO"}

    @classmethod
    def poll(cls, context):
        return "Clip" in bpy.data.objects or context.active_object

    def execute(self, context):
        clip_obj = bpy.data.objects["Clip"] or context.active_object
        bbox_corners = [
            clip_obj.matrix_world @ mathutils.Vector(corner)
            for corner in clip_obj.bound_box
        ]

        bbox_min = [min(corner[i] for corner in bbox_corners) for i in range(3)]
        bbox_max = [max(corner[i] for corner in bbox_corners) for i in range(3)]

        def is_vertex_inside_bbox(vertex, bbox_min, bbox_max):
            return all(bbox_min[i] <= vertex[i] <= bbox_max[i] for i in range(3))

        for obj in context.scene.objects:
            if obj.type != "MESH":
                continue
            mat = obj.matrix_world
            for v in obj.data.vertices:
                real_pos = mat @ v.co
                if is_vertex_inside_bbox(real_pos, bbox_min, bbox_max):
                    try:
                        obj.hide_set(False)
                    except RuntimeError:
                        pass
                    break
            else:
                try:
                    obj.hide_set(True)
                except RuntimeError:
                    pass
        return {"FINISHED"}
