import bpy


class GU_OT_IFC_PCV_store_settings(bpy.types.Operator):
    bl_idname = "ifc.clear_ifc_data"
    bl_label = "Clear IFC Data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        try:
            bpy.ops.bim.purge_ifc_links()
        except AttributeError:
            pass
        bpy.data.batch_remove(bpy.data.objects)
        bpy.data.batch_remove(bpy.data.collections)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {"FINISHED"}
