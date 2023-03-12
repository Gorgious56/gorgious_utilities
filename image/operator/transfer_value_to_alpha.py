import bpy
from bpy.types import Operator
from bpy.props import StringProperty
import numpy as np


class GU_OT_image_transfer_value_to_alpha(Operator):
    bl_idname = "gu.image_transfer_value_to_alpha"
    bl_label = "Transfer Value to Alpha"

    def execute(self, context):
        source_image = context.source_image
        target_image = context.target_image
        if not source_image or not target_image:
            return {"FINISHED"}
        if [a for a in source_image.size] != [a for a in target_image.size]:

            self.report({"WARNING"}, "Image sizes should be the same")
            return {"FINISHED"}

        source_pixels = np.empty(source_image.size[0] * source_image.size[1] * 4, dtype=np.float32)
        source_image.pixels.foreach_get(source_pixels)
        target_pixels = np.empty(source_image.size[0] * source_image.size[1] * 4, dtype=np.float32)
        for i in range(3, len(target_pixels), 4):
            target_pixels[i] = source_pixels[i - 3]
        target_image.pixels.foreach_set(target_pixels)

        return {"FINISHED"}
