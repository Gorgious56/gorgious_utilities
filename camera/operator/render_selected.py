import bpy
from pathlib import Path


class GU_OT_cameras_render_selected(bpy.types.Operator):
    bl_idname = "cameras.render_selected"
    bl_label = "Render Selected Cameras"
    bl_options = {"UNDO"}

    def execute(self, context):
        selected_cameras = [o for o in context.selected_objects if o.type == "CAMERA"]
        scene = context.scene
        layer = context.view_layer
        old_cam = scene.camera
        folder = Path(bpy.data.filepath).parent
        compositor_nodes = scene.node_tree.nodes
        layer_node = next((n for n in compositor_nodes if isinstance(n, bpy.types.CompositorNodeRLayers)), None)
        if layer_node is None:
            print("Error : Please add a View Layer node to the compositor workspace")
            return {"FINISHED"}
        old_filepath = scene.render.filepath
        old_layer = layer_node.layer
        layer_node.layer = layer.name
        for cam in selected_cameras:
            scene.camera = cam
            output_filepath = folder / "Renders" / (cam.name + ".png")
            scene.render.filepath = str(output_filepath)

            bpy.ops.render.render(write_still=True, use_viewport=True, scene=scene.name, layer=layer.name)
        print("Finished rendering")
        scene.camera = old_cam
        scene.render.filepath = old_filepath
        layer_node.layer = old_layer
        return {"FINISHED"}
