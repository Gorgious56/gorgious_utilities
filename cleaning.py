import bpy
from bpy.types import (
    Panel,
    Operator,
)
from bpy.props import(
    EnumProperty,
)


class GU_PT_clean_scene(Panel):
    bl_label = "Cleaning"
    bl_idname = "GU_PT_clean_scene"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(GU_OT_clean_faulty_drivers.bl_idname)
        layout.operator(GU_OT_update_all_drivers.bl_idname)
        layout.operator(GU_OT_remove_fake_users.bl_idname)
        layout.operator(GU_OT_remove_single_empties.bl_idname)


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


def retrieve_data_to_clear(self, context):
    retrieve_data_to_clear.all = 'All'
    items = [(retrieve_data_to_clear.all,)*3]
    for d in dir(bpy.data):
        if "bpy_prop_collection" in str(type(getattr(bpy.data, d))):
            items.append((d, d.capitalize(), d))
    return items


class GU_OT_remove_fake_users(bpy.types.Operator):
    """Remove 'use fake user' properties from selected data containers"""

    bl_idname = "clean.remove_fake_users"
    bl_label = "Remove Fake Users"
    bl_options = {"UNDO"}

    data_to_clear: EnumProperty(
        name="Data to Clear",
        description="Choose which data container to clear all fake users",
        items=retrieve_data_to_clear,)

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        cols_to_clear = []
        if self.data_to_clear == retrieve_data_to_clear.all:
            for d in dir(bpy.data):
                if "bpy_prop_collection" in str(type(getattr(bpy.data, d))):
                    cols_to_clear.append(d)
        else:
            cols_to_clear.append(self.data_to_clear)
        for col in cols_to_clear:
            for e in getattr(bpy.data, col):
                if hasattr(e, "use_fake_user"):
                    e.use_fake_user = False
        return {"FINISHED"}


class GU_OT_remove_single_empties(bpy.types.Operator):
    """Remove empties with no parenting hierarchy attached"""

    bl_idname = "clean.remove_single_empties"
    bl_label = "Remove Single Empties"
    bl_options = {"UNDO"}

    def execute(self, context):
        empties = [o for o in bpy.data.objects if o.type == 'EMPTY' and o.parent is None]
        for o in bpy.data.objects:
            if o.parent in empties:
                empties.remove(o.parent)

        bpy.ops.object.select_all(action='DESELECT')
        [e.select_set(True) for e in empties]
        bpy.ops.object.delete()
        return {"FINISHED"}
