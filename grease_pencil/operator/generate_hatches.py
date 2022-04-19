"""
Running this script will create arrays of images
Which can then be used as "Textures" in Grease Pencil materials
Each array features varying sizes of shapes
Currently there are Disc, Squares and Stripes.
"""

import bpy
from gorgious_utilities.grease_pencil.helper.hatch import GPHatchGenerator



class GU_OT_gpencil_generate_hatches(bpy.types.Operator):
    bl_idname = "gpencil.generate_hatches"
    bl_label = "Generate Hatches"
    bl_options = {"REGISTER", "UNDO"}

    texture_size: bpy.props.IntProperty(default=150, name="Texture Size")
    use_fake_user: bpy.props.BoolProperty(default=True, name="Enforce Fake User")

    def execute(self, context):
        hatch_generator = GPHatchGenerator(self.texture_size)
        hatch_generator.generate_all_hatches()
        for image in hatch_generator.images:
            image.use_fake_user = self.use_fake_user
        return {"FINISHED"}
