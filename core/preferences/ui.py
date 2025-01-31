from bpy.types import AddonPreferences


class AssetBrowserUtilitiesAddonPreferences(AddonPreferences):
    bl_idname = "gorgious_utilities"

    def draw(self, context):
        layout = self.layout
