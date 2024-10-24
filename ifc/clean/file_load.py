import bpy
from collections import defaultdict
from pathlib import Path

try:
    import bonsai
except:
    pass


SCENE_COLLECTION_ALIAS = "__SCENE_COLLECTION_ALIAS__afboisdjk"


def clear_ifc_data(context):
    col_names_to_guids = defaultdict(list)  # Used to re-map entities to custom collections
    blend_col_names_to_ifc_col_names = defaultdict(list)  # Used to re-map Ifc collections to custom collections

    col_parent_map = defaultdict(list)

    for parent in bpy.data.collections:
        if parent.name.startswith("Ifc"):
            continue
        for child in parent.children:
            col_parent_map[child].append(parent)
            if child.name.startswith("Ifc"):
                blend_col_names_to_ifc_col_names[parent.name].append(child.name)

    objs_to_remove = set()
    collection = next((c for c in bpy.data.collections if c.name.startswith("IfcProject")), None)
    if collection:
        for obj in collection.all_objects:
            if getattr(obj, "BIMObjectProperties", None) and obj.BIMObjectProperties.ifc_definition_id:
                if len(obj.users_collection) > 1:
                    entity = bonsai.tool.Ifc.get_entity(obj)
                    if entity:
                        for col in obj.users_collection:
                            if col.name.startswith("Ifc"):
                                continue
                            if col == context.scene.collection:
                                col_names_to_guids[SCENE_COLLECTION_ALIAS].append(entity.GlobalId)
                            else:
                                col_names_to_guids[col.name].append(entity.GlobalId)
                            objs_to_remove.add(obj)
                    else:
                        collection.objects.unlink(obj)
            else:
                # Non ifc objects in ifc collections. Move them out before deleting.
                if len(obj.users_collection) == 1:
                    context.scene.collection.objects.link(obj)

    for child in bpy.data.collections:
        if not child.name.startswith("Ifc"):
            continue
        child.use_fake_user = False
        for parent in col_parent_map[child]:
            parent.children.unlink(child)
        try:
            bpy.data.collections.remove(child)
        except ReferenceError:
            pass

    annotations_to_update = set()
    for obj in bpy.data.objects:
        dxf_props = getattr(obj, "DXFExporterProps")
        if not dxf_props:
            return
        annotation = dxf_props.annotation
        for attribute in annotation.linked_attributes:
            if attribute.target_global_id:
                annotations_to_update.add(obj)
                target = attribute.target_
                if not target:
                    continue
                objs_to_remove.add(target)
                for col in target.users_collection:
                    try:
                        bpy.data.collections.remove(col)
                    except ReferenceError:
                        pass

    if objs_to_remove:
        bpy.data.batch_remove(list(objs_to_remove))

    try:
        bpy.ops.bim.convert_to_blender()
    except AttributeError:
        pass
    else:
        # if collection:
        #     bpy.data.collections.remove(collection)
        bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

    return col_names_to_guids, blend_col_names_to_ifc_col_names, annotations_to_update


class GU_OT_IFC_clear_ifc_data(bpy.types.Operator):
    bl_idname = "gu.ifc_clear_data"
    bl_label = "IFC : Clear Data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        clear_ifc_data(context)
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
        col_names_to_guids, blend_col_names_to_ifc_col_names, annotations_to_update = clear_ifc_data(context)
        use_relative_path = not Path(filepath).exists()
        # Replacement for apparent bug in bonsai https://github.com/IfcOpenShell/IfcOpenShell/issues/5407
        # bpy.ops.bim.load_project(
        #     "EXEC_DEFAULT", should_start_fresh_session=False, filepath=filepath, use_relative_path=use_relative_path
        # )
        if use_relative_path:
            filepath = str(Path(bpy.data.filepath).parent / filepath)
        bpy.ops.bim.load_project("EXEC_DEFAULT", should_start_fresh_session=False, filepath=filepath)
        self.place_entities_in_custom_collections(context, col_names_to_guids)
        self.link_ifc_collections_to_custom_collections(blend_col_names_to_ifc_col_names)
        self.update_annotations(annotations_to_update)
        return {"FINISHED"}

    def place_entities_in_custom_collections(self, context, map):
        for col_name, guids in map.items():
            if col_name == SCENE_COLLECTION_ALIAS:
                col = context.scene.collection
            else:
                col = bpy.data.collections[col_name]
            for guid in guids:
                entity = bonsai.tool.Ifc.get_entity_by_id(guid)
                obj = bonsai.tool.Ifc.get_object(entity)
                col.objects.link(obj)

    def link_ifc_collections_to_custom_collections(self, map):
        for blend_col_name, ifc_col_names in map.items():
            blend_col = bpy.data.collections[blend_col_name]
            for ifc_col_name in ifc_col_names:
                ifc_col = bpy.data.collections[ifc_col_name]
                if ifc_col_name not in blend_col.children:
                    blend_col.children.link(ifc_col)

    def update_annotations(self, objects):
        for obj in objects:
            obj.DXFExporterProps.annotation.update()
