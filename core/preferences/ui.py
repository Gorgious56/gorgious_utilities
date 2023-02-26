from bpy.types import AddonPreferences
from bpy.props import PointerProperty, BoolProperty, CollectionProperty

from gorgious_utilities.gpu.prop import GPUPreferences


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "gorgious_utilities"

    gpu: PointerProperty(type=GPUPreferences)

    def draw(self, context):
        layout = self.layout
        self.gpu.draw(layout)
