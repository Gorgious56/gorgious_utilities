import bpy
from gorgious_utilities.collection.tool import remove_from_all_collections


class GU_OT_IFC_clear_ifc_data(bpy.types.Operator):
    bl_idname = "gu.ifc_clear_data"
    bl_label = "IFC : Clear Data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        collection = next((c for c in bpy.data.collections if c.name.startswith("IfcProject")), None)
        if collection:
            for obj in collection.all_objects:
                if not obj.BIMObjectProperties.ifc_definition_id:
                    if obj.name not in context.scene.collection.objects:
                        context.scene.collection.objects.link(obj)
        try:
            bpy.ops.bim.convert_to_blender()
        except AttributeError:
            pass
        else:
            if collection:
                bpy.data.collections.remove(collection)
            bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
        return {"FINISHED"}


class GU_OT_IFC_load_file(bpy.types.Operator):
    bl_idname = "gu.ifc_load_file"
    bl_label = "IFC : Load File"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        bpy.ops.bim.load_project("INVOKE_DEFAULT", should_start_fresh_session=False)
        return {"FINISHED"}


class GU_OT_IFC_reload_file(bpy.types.Operator):
    bl_idname = "gu.ifc_reload_file"
    bl_label = "IFC : Reload File"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        filepath = bpy.data.scenes["Scene"].BIMProperties.ifc_file
        print("ahha")
        bpy.ops.gu.ifc_clear_data()
        bpy.ops.bim.load_project("EXEC_DEFAULT", should_start_fresh_session=False, filepath=filepath)
        return {"FINISHED"}
