import bpy
from gorgious_utilities.collection.helper import get_family_down
from gorgious_utilities.view_layer.helper import get_view_layer_names


class GU_OT_view_layer_toggle_layer_collections(bpy.types.Operator):
    bl_label = "Toggle all layer collections"
    bl_idname = "view_layer.toggle_layer_collections"
    action: bpy.props.EnumProperty(
        items=(
            ("ON",) * 3,
            ("OFF",) * 3,
        ),
        name="Exclusion",
    )
    on_active: bpy.props.BoolProperty(name="Execute on active View Layer", default=True)
    v_l_name: bpy.props.EnumProperty(
        items=lambda self, context: ((v_l_name,) * 3 for v_l_name in get_view_layer_names(context)),
        name="View Layer",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        view_layer = context.view_layer if self.on_active else context.scene.view_layers.get(self.v_l_name)
        exclude = True if self.action == "OFF" else False
        for layer_col in reversed(list(get_family_down(view_layer.layer_collection))):
            layer_col.exclude = exclude
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "on_active", toggle=True)
        if not self.on_active:
            layout.prop(self, "v_l_name")
