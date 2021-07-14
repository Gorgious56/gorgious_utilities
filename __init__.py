"""
Base module required for Blender registration
"""

from .import auto_load


bl_info = {
    "name": "Gorgious Utilities",
    "blender": (2, 93, 0),
    "category": "Object",
    "version": (0, 1, 15),
    "author": "Gorgious56",
    "description": "Add various utility operators",
}


def register():
    auto_load.init()
    auto_load.register()


def unregister():
    auto_load.unregister()
