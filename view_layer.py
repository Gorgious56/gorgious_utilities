import bpy


class GU_OT_view_layer_save_or_load_stored_view(bpy.types.Operator):
    bl_label = "Save or Load View Layer Stored View"
    bl_idname = "view_layer.save_or_load_stored_view"
    index: bpy.props.IntProperty(description="Stored View Index")
    save_or_load: bpy.props.BoolProperty(description= "False : Save, True : Load")

    @classmethod
    def poll(cls, context):
        # Check if at least one View 3D area exists in the current screen
        if any(a for a in context.screen.areas if a.type == "VIEW_3D"):
            return True
        else:
            if bpy.app.version >= (3, 0, 0):
                cls.poll_message_set("No 3D Viewport available")
            return False

    def execute(self, context):
        # Import the POV class from stored views add-on which offers view saving & loading features
        from space_view3d_stored_views.core import POV

        view_3d_area = next(a for a in context.screen.areas if a.type == "VIEW_3D")
        if self.index >= 0:
            view = context.scene.stored_views.view_list[self.index]
        else:
            # We add a new entry since this view layer is not registered
            view = context.scene.stored_views.view_list.add()
            view.name = context.view_layer.name

        pov = POV(self.index)
        pov.view3d = view_3d_area.spaces[0]  # Patching this since it references a wrong space data
        if self.save_or_load:
            pov.update_v3d(view.pov)
        else:
            pov.from_v3d(view.pov)

        return {"FINISHED"}


class GU_PT_view_layer_stored_view(bpy.types.Panel):
    bl_label = "Stored View"
    bl_idname = "GU_PT_view_layer_stored_view"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "view_layer"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        if not hasattr(scene, "stored_views"):
            # Check if add-on is registered
            if hasattr(bpy.types, "VIEW3D_OT_stored_views_initialize"):
                layout.operator("view3d.stored_views_initialize")
            else:
                layout.label(text="\"Stored Views\" add-on is needed to access Stored Views", icon="ERROR")
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


if __name__ == "__main__":
    bpy.utils.register_class(GU_OT_view_layer_save_or_load_stored_view)
    bpy.utils.register_class(GU_PT_view_layer_stored_view)