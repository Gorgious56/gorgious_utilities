import bpy
from bpy.types import (
    Panel,
    Operator,
)


class GU_PT_clean_scene(Panel):
    bl_label = "Cleaning"
    bl_idname = "GU_PT_clean_scene"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        self.layout.operator(GU_OT_clean_faulty_drivers.bl_idname)
        self.layout.operator(GU_OT_update_all_drivers.bl_idname)


class GU_OT_clean_faulty_drivers(Operator):
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
