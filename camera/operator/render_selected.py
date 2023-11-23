import typing
import bpy
from pathlib import Path

from bpy.types import Context, Event


class GU_OT_cameras_render_selected(bpy.types.Operator):
    bl_idname = "cameras.render_selected"
    bl_label = "Render Selected Cameras"
    bl_options = {"UNDO"}
    prefix: bpy.props.StringProperty(name="Prefix", options={"SKIP_SAVE"})

    def invoke(self, context: Context, event: Event):
        if event.shift:
            return context.window_manager.invoke_props_dialog(self)
        else:
            return self.execute(context)

    def execute(self, context):
        selected_cameras = [o for o in context.selected_objects if o.type == "CAMERA"]
        scene = context.scene
        layer = context.view_layer
        old_cam = scene.camera
        folder = Path(bpy.data.filepath).parent
        if scene.node_tree is None:
            print(
                "Error : Please add a Compositing tree node to the compositor workspace"
            )
            return {"FINISHED"}
        compositor_nodes = scene.node_tree.nodes
        layer_node = next(
            (
                n
                for n in compositor_nodes
                if isinstance(n, bpy.types.CompositorNodeRLayers)
            ),
            None,
        )
        if layer_node is None:
            print("Error : Please add a View Layer node to the compositor workspace")
            return {"FINISHED"}
        old_filepath = scene.render.filepath
        old_layer = layer_node.layer
        layer_node.layer = layer.name
        for cam in selected_cameras:
            scene.camera = cam
            file_name = ""
            if self.prefix:
                file_name = str(self.prefix) + "_"
            file_name += cam.name + ".png"
            output_filepath = folder / "Renders" / file_name
            scene.render.filepath = str(output_filepath)

            bpy.ops.render.render(
                write_still=True, use_viewport=True, scene=scene.name, layer=layer.name
            )
        print("Finished rendering")
        scene.camera = old_cam
        scene.render.filepath = old_filepath
        layer_node.layer = old_layer
        return {"FINISHED"}
