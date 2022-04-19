import bpy


def get_or_create_gp_mat(name, show_stroke=True, stroke_color=(0, 0, 0, 1), show_fill=False, fill_color=(0, 0, 0, 1)):
    new_mat = bpy.data.materials.get(name)
    if not new_mat:
        new_mat = bpy.data.materials.new(name)
    if not new_mat.is_grease_pencil:
        bpy.data.materials.create_gpencil_data(new_mat)

    new_mat.grease_pencil.show_stroke = show_stroke
    new_mat.grease_pencil.color = stroke_color
    new_mat.grease_pencil.show_fill = show_fill
    new_mat.grease_pencil.fill_color = fill_color

    return new_mat
