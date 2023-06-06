from bpy.types import Panel
import bpy

try:
    import blenderbim.tool as tool
    import blenderbim.bim.helper
    import blenderbim.bim.module.pset.data.Data
except:
    pass
finally:

    class GU_PT_IFC_PCV(Panel):
        bl_label = "Point Cloud Visualizer"
        bl_space_type = "PROPERTIES"
        bl_region_type = "WINDOW"
        bl_context = "object"

        @classmethod
        def poll(cls, context):
            if not context.active_object:
                return False
            return tool.Ifc.get() and blenderbim.bim.helper.get_obj_ifc_definition_id(
                context, context.active_object.name, "Object"
            )

        def draw(self, context):
            self.draw_store_update(self.layout)

        @staticmethod
        def draw_store_update(layout, obj=None):
            row = layout.row(align=True)
            if obj:
                row.context_pointer_set("active_object", obj)
            row.operator("ifc.pcv_store_settings", icon="IMPORT")
            row.operator("ifc.pcv_update_settings", icon="EXPORT")

    def pcv_topbar_menu(self, context):
        for obj in bpy.context.scene.objects:
            element = tool.Ifc.get_entity(obj)
            if not element:
                continue
            pset = tool.Pset.get_element_pset(element, "PointCloudVisualizerProps")
            if not pset:
                continue
            box = self.layout.box()
            box.label(text=element.Name)
            row = box.row(align=True)
            op = row.operator("gu.select_and_set_active", text="", icon="RESTRICT_SELECT_OFF")
            row.prop(obj, "hide_viewport", text="", icon="HIDE_OFF")
            op.object_name = obj.name
            GU_PT_IFC_PCV.draw_store_update(row, obj)
            row.context_pointer_set("object", obj)
            row.context_pointer_set("active_object", obj)  # Not necessary but keep it if pcv author changes their mind
            row.operator("point_cloud_visualizer.mechanist_draw")
            for prop in pset.HasProperties:
                if prop.Name == "Clip Object Name":
                    value = prop.NominalValue.wrappedValue
                    if value:
                        op = row.operator("gu.select_and_set_active", text="", icon="SNAP_PEEL_OBJECT")
                        op.object_name = value
                    break

    def register():
        bpy.types.PCV_PT_view3d_menu.append(pcv_topbar_menu)

    def unregister():
        try:
            bpy.types.PCV_PT_view3d_menu.remove(pcv_topbar_menu)
        except AttributeError:
            pass
