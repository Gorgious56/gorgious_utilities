import bpy
import numpy as np


class GPHatchGenerator:
    def __init__(self, texture_size) -> None:
        self.size = texture_size, texture_size
        self.width = texture_size
        self.height = texture_size
        self.middle_x = self.size[0] / 2
        self.middle_y = self.size[1] / 2
        self.images = set()

    def generate_all_hatches(self):
        for rad, rad_size in zip((0.1, 0.2, 0.3, 0.4, 0.49), ("10", "20", "30", "40", "50")):
            radius_squared = (rad * min(self.size[0], self.size[1])) ** 2
            self.generate_single_hatch(self.disc_equation, radius_squared, rad_size)
            self.generate_single_hatch(self.square_equation, radius_squared, rad_size)
            self.generate_single_hatch(self.cross_equation, radius_squared, rad_size)
            self.generate_single_hatch(self.band_equation, radius_squared, rad_size)

    def generate_single_hatch(self, is_in_shape, radius_squared, radius_display):
        if is_in_shape == self.disc_equation:
            name = "GP_HATCH_DISC_" + radius_display
        elif is_in_shape == self.square_equation:
            name = "GP_HATCH_SQUARE_" + radius_display
        elif is_in_shape == self.cross_equation:
            name = "GP_HATCH_CROSS_" + radius_display
        elif is_in_shape == self.band_equation:
            name = "GP_HATCH_BAND_" + radius_display
        image = bpy.data.images.get(name)
        if image is None:
            image = bpy.data.images.new(name, width=self.width, height=self.size[1])
        else:
            image.generated_width = self.width
            image.generated_height = self.height
        image.file_format = "PNG"


        pixels_np = np.fromfunction(
            lambda x, y, _: is_in_shape(x, y, radius_squared), (self.width, self.height, 4), dtype=np.float32
        )
        pixels_np = np.ravel(pixels_np).astype(np.float32)
        image.pixels.foreach_set(pixels_np)
        self.images.add(image)

    def disc_equation(self, x, y, radius_squared):
        return ((x - self.middle_x) ** 2 + (y - self.middle_y) ** 2) < radius_squared

    def cross_equation(self, x, y, radius_squared):
        return ((x - self.middle_x) ** 2 < radius_squared) + ((y - self.middle_y) ** 2 < radius_squared)

    def square_equation(self, x, y, radius_squared):
        return ((x - self.middle_x) ** 2 < radius_squared) * ((y - self.middle_y) ** 2 < radius_squared)

    def band_equation(self, x, y, radius_squared):
        return (x - self.middle_x) ** 2 < radius_squared
