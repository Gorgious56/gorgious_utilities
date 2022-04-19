import bpy


def get_grease_pencil_layer(
    gpencil: bpy.types.GreasePencil,
    gpencil_layer_name="GP_Layer",
    clear_layer=False,
) -> bpy.types.GPencilLayer:
    if gpencil.data.layers:
        gpencil_layer = gpencil.data.layers.get(gpencil_layer_name)
        if not gpencil_layer:
            gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)
        elif clear_layer:
            gpencil_layer.clear()
        # bpy.ops.gpencil.paintmode_toggle()  # need to trigger otherwise there is no frame
    else:
        gpencil_layer = gpencil.data.layers.new(gpencil_layer_name, set_active=True)
    return gpencil_layer


def clear_layers(gpencil):
    while gpencil.data.layers:
        gpencil.data.layers.remove(gpencil.data.layers[0])
