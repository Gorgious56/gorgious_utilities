import bpy


class GU_PT_view_layer_stored_view(bpy.types.Panel):
    bl_label = "Stored View"
    bl_idname = "GU_PT_view_layer_stored_view"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "view_layer"

    @classmethod
    def poll(cls, context):
        return False

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        if not hasattr(scene, "stored_views"):
            # Check if add-on is registered
            if hasattr(bpy.types, "VIEW3D_OT_stored_views_initialize"):
                layout.operator("view3d.stored_views_initialize")
            else:
                layout.label(text='"Stored Views" add-on is needed to access Stored Views', icon="ERROR")
                layout.operator("preferences.addon_enable").module = "space_view3d_stored_views"
            return

        view_layer = context.view_layer
        # If the view layer's view has already been saved, we find its entry index
        index = -1
        for i, view in enumerate(scene.stored_views.view_list):
            if view_layer.name == view.name:
                index = i
                break

        row = layout.row()
        save_op = row.operator("view_layer.save_or_load_stored_view", icon="EXPORT", text="Save")
        save_op.index = index
        save_op.save_or_load = False

        sub_row = row.row()
        load_op = sub_row.operator("view_layer.save_or_load_stored_view", icon="IMPORT", text="Load")
        load_op.index = index
        load_op.save_or_load = True
        sub_row.enabled = index >= 0  # Prevent loading view if it doesn't exist

        layout.operator("view_layer.update_stored_view_on_change")
