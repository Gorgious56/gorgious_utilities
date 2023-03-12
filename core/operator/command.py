from bpy.types import Operator
from bpy.props import StringProperty


class GU_OT_command(Operator):
    bl_idname = "gu.command"
    bl_label = ""
    command: StringProperty()

    def execute(self, context):
        import bpy

        exec(self.command)
        return {"FINISHED"}
