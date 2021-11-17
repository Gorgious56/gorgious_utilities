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
