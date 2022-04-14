def get_view_layers(context):
    return [v_l for v_l in context.scene.view_layers]


def get_view_layer_names(context):
    return sorted([v_l.name for v_l in get_view_layers(context)])


def delete_view_layer(context, view_layer_name):
    context.scene.view_layers.remove(context.scene.view_layers.get(view_layer_name))
