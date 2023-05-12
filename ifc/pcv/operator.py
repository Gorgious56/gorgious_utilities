import bpy
from mathutils import Matrix
import json

try:
    from ifcopenshell.api import run
    from blenderbim.bim.ifc import IfcStore
    import blenderbim.tool as tool
except:
    pass
finally:
    pcv_mapping_dict = {
        "File Path": ("point_cloud_visualizer.load", "filepath"),
        "Shader": ("point_cloud_visualizer.shader", "type"),
        "Percentage": ("point_cloud_visualizer.display", "percentage"),
        "Point Size": ("point_cloud_visualizer.display", "point_size"),
        "Alpha": ("point_cloud_visualizer.display", "global_alpha"),
        "Clip": ("point_cloud_visualizer.shader", "clip_enabled"),
        "Clip Planes Live Update": ("point_cloud_visualizer.shader", "clip_planes_from_bbox_object_live"),
        "Use Scalars": ("point_cloud_visualizer.display", "use_scalar"),
        "Scalar Use Scheme": ("point_cloud_visualizer.display", "use_scheme"),
        "Scalar Scheme": ("point_cloud_visualizer.display", "scheme"),
        "Scalar Opacity": ("point_cloud_visualizer.display", "bleeding"),
        "Scalar Mode": ("point_cloud_visualizer.display", "blending_mode"),
    }

    class GU_OT_IFC_PCV_update_settings(bpy.types.Operator):
        bl_idname = "ifc.pcv_update_settings"
        bl_label = "Update PCV Settings"
        bl_options = {"REGISTER", "UNDO"}

        @classmethod
        def poll(cls, context):
            obj = context.active_object
            if obj is None:
                return
            element = tool.Ifc.get_entity(obj)
            if not element:
                return
            return bool(tool.Pset.get_element_pset(element, "PointCloudVisualizerProps"))

        def execute(self, context):
            obj = context.active_object
            element = tool.Ifc.get_entity(obj)
            pset = tool.Pset.get_element_pset(element, "PointCloudVisualizerProps")
            print(pset)
            for prop in pset.HasProperties:
                value = prop.NominalValue.wrappedValue
                if prop.Name == "Clip Object Name":
                    if not value:
                        continue
                    obj_clip = bpy.data.objects.get(value)
                    if not obj_clip:
                        bpy.ops.mesh.primitive_cube_add(
                            size=2, enter_editmode=False, align="WORLD", location=(0, 0, 0), scale=(1, 1, 1)
                        )
                        context.active_object.name = value
                        obj_clip = context.active_object
                        obj_clip.display_type = "BOUNDS"
                        obj_clip.select_set(False)
                        context.view_layer.objects.active = obj
                        obj.select_set(True)
                    obj.point_cloud_visualizer.shader.clip_planes_from_bbox_object = obj_clip
                    clip_obj_matrix_prop = next(
                        (p for p in pset.HasProperties if p.Name == "Clip Object Matrix"), None
                    )
                    if clip_obj_matrix_prop:
                        matrix_1d = json.loads(clip_obj_matrix_prop.NominalValue.wrappedValue)
                        matrix = [
                            (
                                matrix_1d[4 * i],
                                matrix_1d[4 * i + 1],
                                matrix_1d[4 * i + 2],
                                matrix_1d[4 * i + 3],
                            )
                            for i in range(4)
                        ]
                        obj_clip.matrix_world = Matrix(matrix)

                elif prop.Name == "Scalar Range Min":
                    obj.point_cloud_visualizer.display.range[0] = value
                elif prop.Name == "Scalar Range Max":
                    obj.point_cloud_visualizer.display.range[1] = value
                elif prop.Name in pcv_mapping_dict:
                    prop_path, attr = pcv_mapping_dict[prop.Name]
                    setattr(obj.path_resolve(prop_path), attr, value)

            return {"FINISHED"}

    class GU_OT_IFC_PCV_store_settings(bpy.types.Operator):
        bl_idname = "ifc.pcv_store_settings"
        bl_label = "Store PCV Settings"
        bl_options = {"REGISTER", "UNDO"}

        def execute(self, context):
            obj = context.active_object
            ifc = tool.Ifc.get()
            element = tool.Ifc.get_entity(obj)

            pset = run("pset.add_pset", ifc, product=element, name="PointCloudVisualizerProps")

            properties = {k: getattr(obj.path_resolve(v[0]), v[1]) for k, v in pcv_mapping_dict.items()}
            clip_object = obj.point_cloud_visualizer.shader.clip_planes_from_bbox_object
            properties["Clip Object Name"] = clip_object.name if clip_object else None
            if clip_object:
                rows = clip_object.matrix_world.row
                matrix_1d = []
                for row in rows:
                    for elt in row:
                        matrix_1d.append(elt)
                properties["Clip Object Matrix"] = json.dumps(matrix_1d)
            properties["Scalar Range Min"] = obj.point_cloud_visualizer.display.range[0]
            properties["Scalar Range Max"] = obj.point_cloud_visualizer.display.range[1]

            run("pset.edit_pset", ifc, pset=pset, properties=properties)
            ifc.write(IfcStore.path)

            context.view_layer.objects.active = context.active_object

            return {"FINISHED"}
