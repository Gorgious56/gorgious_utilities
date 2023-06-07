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
        collection = next((c for c in bpy.data.collections if c.name.startswith("IfcProject")), None)
        if collection:
            bpy.data.collections.remove(collection)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {"FINISHED"}
