import bpy


def add_driver_to(obj, prop_to, variables, expression=None):
    """
    Add a driver to obj's prop_to property
    """
    if not obj:
        return
    try:
        if isinstance(prop_to, dict):
            driver = obj.driver_add(prop_to["attr"], prop_to["dim"]).driver
        else:
            driver = obj.driver_add(prop_to).driver
    except (TypeError, AttributeError) as e:
        print(e)
        return
    for i, var_prop in enumerate(variables):
        try:
            var = driver.variables[i]
        except IndexError:
            var = driver.variables.new()
        var.name = var_prop[0]
        var.type = "SINGLE_PROP"

        target = var.targets[0]
        target.id_type = var_prop[1]
        target.id = var_prop[2]
        target.data_path = str(var_prop[3])

    if expression is not None:
        driver.expression = expression
    else:
        driver.expression = variables[0][0]


def remove_all_drivers():
    for obj in bpy.data.objects:
        if not hasattr(obj, "drivers"):
            continue
        drivers_data = obj.animation_data.drivers
        if not drivers_data:
            continue
        for dr in drivers_data:
            obj.driver_remove(dr.data_path, -1)
