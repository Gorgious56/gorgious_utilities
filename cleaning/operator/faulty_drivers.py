import bpy


class GU_OT_clean_faulty_drivers(bpy.types.Operator):
    """Removes all invalid drivers from file"""

    bl_idname = "clean.faulty_drivers"
    bl_label = "Clean Drivers"
    bl_options = {"UNDO"}

    def execute(self, context):
        data = bpy.data
        colls = [p for p in dir(data) if isinstance(getattr(data, p), bpy.types.bpy_prop_collection)]

        for p in colls:
            for ob in getattr(data, p, []):
                ad = getattr(ob, "animation_data", None)
                if not ad:
                    continue
                bung_drivers = []
                # Find bung drivers
                for d in ad.drivers:
                    try:
                        ob.path_resolve(d.data_path)
                    except ValueError:
                        bung_drivers.append(d)
                # Remove bung drivers
                while bung_drivers:
                    ad.drivers.remove(bung_drivers.pop())
        return {"FINISHED"}