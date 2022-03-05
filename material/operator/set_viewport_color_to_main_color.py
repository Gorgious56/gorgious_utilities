import bpy
from gorgious_utilities.material.helper import update_viewport_color


class GU_OT_set_viewport_color_to_main_color(bpy.types.Operator):
    bl_idname = "material.set_viewport_color_to_main_color"
    bl_label = "Update Viewport Color"
    bl_options = {"UNDO"}

    filter_materials: bpy.props.EnumProperty(
        name="Materials",
        items=(
            ("CONTEXT", "Active Material", ""),
            ("OBJECT", "Selected Objects", ""),
            ("ALL", "All Materials", ""),
        ),
        default="CONTEXT",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        mats = set()
        if self.filter_materials == "CONTEXT":
            mats.add(context.material)
        elif self.filter_materials == "OBJECT":
            for obj in context.selected_objects:
                for mat_slot in obj.material_slots:
                    print(mat_slot.material)
                    mats.add(mat_slot.material)
        elif self.filter_materials == "ALL":
            for mat in bpy.data.materials:
                mats.add(mat)
        for mat in mats:
            update_viewport_color(mat)
        return {"FINISHED"}
