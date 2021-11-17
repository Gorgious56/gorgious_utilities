import bpy
from gorgious_utilities.modifier.helper import (
    are_any_objs_synched,
    remove_drivers,
)
from gorgious_utilities.event.watcher import (
    EventWatcher,
    parent_watchers,
)



class GU_OT_modifier_desync(bpy.types.Operator):
    """Desynchronize Modifiers"""
    bl_idname = "modifier.desync"
    bl_label = "Desynchronize"
    
    @classmethod
    def poll(cls, context):
        return are_any_objs_synched(context.selected_objects)


    def execute(self, context):
        for obj in context.selected_objects:
            watchers = parent_watchers(obj)
            if not watchers:
                continue
            for w in watchers:
                if obj == w.context:
                    EventWatcher.remove_watcher(w)
                    continue
                watcher_driven_objs = w.callback_args["selected_objects"]
                if obj in watcher_driven_objs:
                    watcher_driven_objs.remove(obj)
                    remove_drivers(obj)
                    if not watcher_driven_objs:
                        EventWatcher.remove_watcher(w)
        return {'FINISHED'}