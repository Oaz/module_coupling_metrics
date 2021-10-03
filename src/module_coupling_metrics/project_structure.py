"""Core entities describing a project structure."""

from typing import Dict

class Class:
    name: str

    def __init__(self, name):
        self.name = name
        self.base_classes = []
        self.descendant_classes = []


class Module:
    name: str
    classes: Dict[str, Class]

    def __init__(self, name, classes=[]):
        self.name = name
        self.classes = dict([(c.name, c) for c in classes])
        self.imports = []
        self.imported_by = []

class Project:
    name: str
    modules: Dict[str, Module]
    all_classes: Dict[str, Class]

    def __init__(self, name, modules=[]):
        self.name = name
        self.modules = dict([(m.name, m) for m in modules])
        self.all_classes = dict()

    def gather_all_classes(self):
        self.all_classes = dict(
            [(cls.name, cls) for (_, module) in self.modules.items() for (_, cls) in module.classes.items()])

    def compute_descendant_classes(self):
        for (_, cls) in self.all_classes.items():
            cls.descendant_classes = []
        for (_, cls) in self.all_classes.items():
            for base_cls in cls.base_classes:
                base_cls.descendant_classes.append(cls)
