class Component:

    def __init__(self, instability, abstractness):
        self.instability = instability
        self.abstractness = abstractness
        self.distance_from_main_sequence = abs(self.abstractness + self.instability - 1)


def compute(project):
    def zero_if_error(v):
        try:
            return v()
        except:
            return 0

    def module_to_component(module):
        fan_in = len(module.imported_by)
        fan_out = len(module.imports)
        abstract_classes = len([cls for (_, cls) in module.classes.items() if len(cls.descendant_classes) > 0])
        all_classes = len(module.classes)
        return Component(
            zero_if_error(lambda: fan_out / (fan_out + fan_in)),
            zero_if_error(lambda: abstract_classes / all_classes)
        )

    return dict([(module.name, module_to_component(module)) for (_, module) in project.modules.items()])
