from typing import Set
import bpy
from bpy.types import Context, Event


class GU_OT_python_install_library(bpy.types.Operator):
    bl_idname = "gu.python_install_library"
    bl_label = "Install Python Library / Module"
    bl_options = {"UNDO", "REGISTER"}
    library_name : bpy.props.StringProperty(name="Module Name")

    def execute(self, context):
        if self.library_name:
            import subprocess
            import sys
            from pathlib import Path

            py_exec = str(sys.executable)
            # Get lib directory
            lib = Path(py_exec).parent.parent / "lib"
            # Ensure pip is installed
            subprocess.call([py_exec, "-m", "ensurepip", "--user" ])
            # Update pip (not mandatory)
            subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip" ])
            # Install packages
            subprocess.call([py_exec,"-m", "pip", "install", f"--target={str(lib)}", self.library_name])
        return {"FINISHED"}
