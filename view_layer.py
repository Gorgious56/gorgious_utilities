import bpy


class GU_OT_view_layer_load_stored_view(bpy.types.Operator):
    bl_label = "Load View Layer Stored View"
    bl_idname = "view_layer.load_stored_view"
    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        if any(a for a in context.screen.areas if a.type == "VIEW_3D"):
            return True
        else:
            cls.poll_message_set("No 3D Viewport available")
            return False


    def execute(self, context):
        from space_view3d_stored_views.core import POV

        view_3d_area = next(a for a in context.screen.areas if a.type == "VIEW_3D")
        view = context.scene.stored_views.view_list[self.index]

        pov = POV(self.index)
        pov.view3d = view_3d_area.spaces[0] # Patching this since it references a wrong space data
        pov.update_v3d(view.pov)

        return {"FINISHED"}


class GU_OT_view_layer_save_stored_view(bpy.types.Operator):
    bl_label = "Save View Layer Stored View"
    bl_idname = "view_layer.save_stored_view"
    index: bpy.props.IntProperty()

    @classmethod
    def poll(cls, context):
        if any(a for a in context.screen.areas if a.type == "VIEW_3D"):
            return True
        else:
            cls.poll_message_set("No 3D Viewport available")
            return False


    def execute(self, context):
        from space_view3d_stored_views.core import POV

        view_3d_area = next(a for a in context.screen.areas if a.type == "VIEW_3D")
        if self.index >= 0:
            view = context.scene.stored_views.view_list[self.index]
        else:
            view = context.scene.stored_views.view_list.add()
            view.name = context.view_layer.name

        pov = POV(self.index)
        pov.view3d = view_3d_area.spaces[0] # Patching this since it references a wrong space data
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
            if hasattr(bpy.types, "VIEW3D_OT_stored_views_initialize"):
                layout.operator("view3d.stored_views_initialize")
            else:
                layout.label(text="\"Stored Views\" add-on is needed to access Stored Views", icon="ERROR")
                layout.operator("preferences.addon_enable").module = "space_view3d_stored_views"
            return
        
        view_layer = context.view_layer
        index = -1
        for i, view in enumerate(scene.stored_views.view_list):
            if view_layer.name == view.name:
                index = i
                break
        row = layout.row()
        row.operator("view_layer.save_stored_view", icon="EXPORT", text="Save").index = index
        sub_row = row.row()
        sub_row.operator("view_layer.load_stored_view", icon="IMPORT", text="Load").index = index
        sub_row.enabled = index >= 0
