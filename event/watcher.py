class EventWatcher:
    _watchers = []

    @property
    def watchers(self):
        return self._watchers

    @staticmethod
    def add_watcher(watcher):
        EventWatcher._watchers.append(watcher)

    @staticmethod
    def remove_watcher(watcher):
        if watcher.callback_onremove:
            watcher.callback_onremove(watcher)
        EventWatcher._watchers.remove(watcher)

    @staticmethod
    def remove_all_watchers():
        EventWatcher._watchers.clear()

    def __init__(
        self, context, path, comparer, callback_onfire, callback_args, callback_onremove=None, copy_method=None
    ):
        self.context = context
        self.path = path
        self.copy_method = copy_method
        self.comparer = comparer
        self.callback_onfire = callback_onfire
        self.callback_args = callback_args
        self.callback_onremove = callback_onremove
        self.current_value = self.get_value()

    def get_value(self):
        split_path = self.path.split(".")
        attr_path = split_path[0]
        try:
            if not hasattr(self.context, attr_path):
                print(f"Error : {self.context} does not have any attribute named {attr_path}")
                return None
        except ReferenceError:
            print("Watcher context does not exist anymore. Desynchronizing...")
            EventWatcher.remove_watcher(self)
            return
        value = getattr(self.context, split_path[0])  # Access 1st member of the property path
        for depth in range(len(split_path[1::])):  # Iteratively access the other members
            attr_path = split_path[depth + 1]
            if not hasattr(value, attr_path):
                print(f"Error : {value} does not have any attribute named {attr_path}")
                break
            value = getattr(value, attr_path)
        if self.copy_method and hasattr(value, self.copy_method):
            value = getattr(value, self.copy_method)()
        return value

    def fire(self, force=False):
        new_value = self.get_value()
        if new_value is not None and not self.comparer(self.current_value, new_value) or force:
            self.current_value = new_value
            self.callback_onfire(self)


def cb_scene_update(context):
    [ew.fire() for ew in reversed(EventWatcher._watchers)]


def parent_watchers(obj):
    watchers = []
    for w in EventWatcher._watchers:
        if obj in w.callback_args["selected_objects"] or obj == w.context:
            watchers.append(w)
    return watchers
