import bpy


class GU_OT_update_all_drivers(bpy.types.Operator):
    """Updates all drivers in scene"""

    bl_idname = "clean.update_drivers"
    bl_label = "Update Drivers"
    bl_options = {"UNDO"}

    def execute(self, context):
        data = bpy.data
        colls = [p for p in dir(data) if isinstance(getattr(data, p), bpy.types.bpy_prop_collection)]

        for p in colls:
            for ob in getattr(data, p, []):
                ad = getattr(ob, "animation_data", None)
                if not ad:
                    continue
                for d in ad.drivers:
                    try:
                        ob.path_resolve(d.data_path)
                    except ValueError:
                        pass
        return {"FINISHED"}
