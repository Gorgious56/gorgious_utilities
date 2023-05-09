import bpy


pcv_mapping_dict = {
    "File Path": ("point_cloud_visualizer.load", "filepath"),
    "Use Scalars": ("point_cloud_visualizer.display", "use_scalar"),
}


class GU_OT_IFC_PCV_update_settings(bpy.types.Operator):
    bl_idname = "ifc.pcv_update_settings"
    bl_label = "Update PCV Settings"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        obj = context.active_object
        from blenderbim.bim.module.pset.data import ObjectPsetsData

        if not ObjectPsetsData.is_loaded:
            ObjectPsetsData.load()

        for pset in ObjectPsetsData.data["psets"]:
            if "PointCloudVisualizer" in pset["Name"]:
                for prop in pset["Properties"]:
                    if prop["Name"] in pcv_mapping_dict:
                        prop_path, attr = pcv_mapping_dict[prop["Name"]]
                        setattr(obj.path_resolve(prop_path), attr, prop["NominalValue"])

        return {"FINISHED"}
