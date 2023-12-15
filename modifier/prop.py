from bpy.props import CollectionProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup, GeometryNodeTree
from gorgious_utilities.core.prop import GUPropsObject


class ModifierInputState(PropertyGroup):
    show: BoolProperty(default=True)


class ModifierInputs(PropertyGroup):
    inputs: CollectionProperty(type=ModifierInputState)

    def draw(self, layout):
        for input in self.inputs:
            row = layout.row()
            row.label(text=input.name)
            row.prop(input, "show")


class ModifierProps(PropertyGroup):
    modifier_inputs: CollectionProperty(type=ModifierInputs)


GUPropsObject.__annotations__["modifier"] = PointerProperty(type=ModifierProps)


def register():
    @property
    def inputs(tree):
        return [
            s
            for s in tree.interface.items_tree
            if getattr(s, "in_out", "Panel") == "INPUT"
        ]

    GeometryNodeTree.inputs = inputs

    @property
    def outputs(tree):
        return [
            s
            for s in tree.interface.items_tree
            if getattr(s, "in_out", "Panel") == "OUTPUT"
        ]

    GeometryNodeTree.outputs = outputs
