import bpy
from gorgious_utilities.event.watcher import (
    EventWatcher,
    cb_scene_update,
    parent_watchers,
)
from gorgious_utilities.modifier.helper import (
    are_modifiers_same,
    copy_modifiers,
    remove_drivers_objs,
)


class GU_OT_modifier_sync(bpy.types.Operator):
    """Synchronize modifiers"""

    bl_idname = "modifier.sync"
    bl_label = "Synchronize"

    def execute(self, context):
        if cb_scene_update in bpy.app.handlers.depsgraph_update_post:
            bpy.app.handlers.depsgraph_update_post.remove(cb_scene_update)

        active_object = context.object
        selected_objects_minus_active = set(context.view_layer.objects.selected[:])
        selected_objects_minus_active.remove(active_object)

        watchers = parent_watchers(active_object)
        if watchers:
            for w in watchers:
                if active_object != w.context:
                    continue
                EventWatcher.remove_watcher(w)

        new_event = EventWatcher(
            context=context.object,
            path="modifiers",
            comparer=are_modifiers_same,
            callback_onfire=lambda w: copy_modifiers(w.context, w.callback_args["selected_objects"], True, True),
            callback_args={"selected_objects": selected_objects_minus_active},
            callback_onremove=lambda w: remove_drivers_objs(w.callback_args["selected_objects"]),
            copy_method="values",
        )
        EventWatcher.add_watcher(new_event)
        bpy.app.handlers.depsgraph_update_post.append(cb_scene_update)
        new_event.fire(force=True)
        return {"FINISHED"}
