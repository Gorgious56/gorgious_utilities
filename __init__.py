"""
Base module required for Blender registration
"""

from .import auto_load

bl_info = {
    "name": "Gorgious Utilities",
    "author": "Gorgious",
    "description":
        """Multiple Utilities""",
    "blender": (2, 93, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Misc"
}


def register():
    auto_load.init()
    auto_load.register()


def unregister():
    auto_load.unregister()
