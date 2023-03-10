import bpy


def create_image(**kwargs):
    return bpy.data.images.new(**kwargs)
