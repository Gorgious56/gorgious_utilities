from bpy.props import StringProperty, BoolProperty, FloatProperty
from bpy.types import PropertyGroup

from gorgious_utilities.core.property.tool import display_name


class TextureSetting(PropertyGroup):
    name: StringProperty()
    image_size: FloatProperty(default=1, min=0.01, soft_min=1, soft_max=8, step=100, precision=1)
    use_alpha: BoolProperty(default=False)
    bake_me: BoolProperty(default=True)
    active: BoolProperty(default=True)

    @property
    def pixel_size(self):
        return int(self.image_size * 1024)

    def draw(self, layout, index=None):
        if self.bake_me:
            layout.prop(self, "image_size", text=display_name(self, "image_size"))
        layout.prop(self, "bake_me", text="", icon="TEXTURE")
        layout.prop(self, "use_alpha", text="", icon="IMAGE_RGB_ALPHA")
        layout.prop(self, "active", icon="UNLINKED", text="")
