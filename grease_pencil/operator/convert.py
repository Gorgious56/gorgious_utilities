import bpy
from gorgious_utilities.collection.helper import get_family_down, get_family_names
from gorgious_utilities.grease_pencil.helper import convert_gpencil_to_curve, convert_gpencil_to_mesh


# def retrieve_col_names(self, context):
#     for col in bpy.data.collections:
#         yield (col.name, ) * 3


class GU_OT_GP_convert(bpy.types.Operator):
    bl_idname = "grease_pencil.convert"
    bl_label = "Convert Grease Pencil Object"
    bl_options = {"REGISTER", "UNDO"}

    mode: bpy.props.EnumProperty(
        name="Convert to",
        items=(
            ("MESH",) * 3,
            ("CURVE",) * 3,
        ),
    )
    # collection_mode: bpy.props.EnumProperty(
    #     name="Target Collection",
    #     items=(
    #         ("GP", "Same as GP Object", ""),
    #         ("Custom",) * 3,
    #     ),
    # )
    # collection_custom: bpy.props.EnumProperty(name="Collection", items=retrieve_col_names)
    flatten_layers: bpy.props.BoolProperty(name="Flatten Layers", default=True)

    @classmethod
    def poll(cls, context):
        return any(o.type == "GPENCIL" for o in context.selected_objects)

    def execute(self, context):
        depsgraph = context.evaluated_depsgraph_get()
        gpencil_selected = (o for o in context.selected_objects if o.type == "GPENCIL")
        bpy.ops.object.select_all(action="DESELECT")
        for o in gpencil_selected:
            if o.type != "GPENCIL":
                continue
            o_eval = o.evaluated_get(depsgraph)
            convert = convert_gpencil_to_curve if self.mode == "CURVE" else convert_gpencil_to_mesh
            objs = list(
                convert(gpencil_object=o_eval, flatten_layers=self.flatten_layers, collection=o.users_collection[0])
            )
            for obj in objs:
                obj.select_set(True)
            context.view_layer.objects.active = objs[0]
        return {"FINISHED"}

    def invoke(self, context, events):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "mode")
        layout.prop(self, "flatten_layers")
        # layout.prop(self, "collection_mode")
        # layout.prop(self, "collection_custom")
