import bpy
import bmesh
import platform
import subprocess

obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data)


def copy2clip(txt):
    cmd = "echo " + txt.strip()
    if platform.system() == "Linux":
        cmd += "|xclip"
    elif platform.system() == "Darwin":
        cmd += "|pbcopy"
    else:
        cmd += "|clip"
    return subprocess.check_call(cmd, shell=True)


for v in bm.verts:
    if v.select:
        idx = v.index
        bpy.ops.object.editmode_toggle()

        attribute = obj.data.attributes["Color"]
        attribute_value = attribute.data[idx].color
        print([c for c in attribute_value])
        copy2clip(str([c for c in attribute_value]))
        bpy.ops.object.editmode_toggle()
        break
