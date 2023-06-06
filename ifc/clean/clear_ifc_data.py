import bpy
from gorgious_utilities.collection.tool import remove_from_all_collections


class GU_OT_IFC_PCV_store_settings(bpy.types.Operator):
    bl_idname = "ifc.clear_ifc_data"
    bl_label = "Clear IFC Data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            bpy.ops.bim.purge_ifc_links()
        except AttributeError:
            pass
        objs_to_delete = set(bpy.data.objects)
        for obj in bpy.data.objects:
            if obj in context.selected_objects or (
                hasattr(obj, "point_cloud_visualizer") and obj.point_cloud_visualizer.load.filepath
            ):
                remove_from_all_collections(obj, link_in_scene_collection=True)
                try:
                    objs_to_delete.remove(obj)
                except:
                    pass
                if clip_obj := obj.point_cloud_visualizer.shader.clip_planes_from_bbox_object:
                    remove_from_all_collections(clip_obj, link_in_scene_collection=True)
                    try:
                        objs_to_delete.remove(clip_obj)
                    except:
                        pass

        bpy.data.batch_remove(objs_to_delete)
        bpy.data.batch_remove(bpy.data.collections)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {"FINISHED"}
