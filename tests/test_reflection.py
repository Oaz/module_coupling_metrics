from unittest import TestCase

from src.module_coupling_metrics.reflection import load_project_structure


class TestLoadProjectStructure(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.names = lambda l: [x.name for x in l]
        cls.project = load_project_structure("./test_data/sample_project")
        cls.imports = lambda _, n: cls.names(cls.project.modules[n].imports)
        cls.imported_by = lambda _, n: cls.names(cls.project.modules[n].imported_by)
        cls.base_classes = lambda _, n: cls.names(cls.project.all_classes[n].base_classes)
        cls.descendant_classes = lambda _, n: cls.names(cls.project.all_classes[n].descendant_classes)

    def test_modules(self):
        self.assertEqual(len(self.project.modules), 8)

    def test_module_imports(self):
        self.assertSequenceEqual(self.imports("sample_project"), ["sample_project.a", "sample_project.x"])
        self.assertSequenceEqual(self.imports("sample_project.x"), ["sample_project.b"])
        self.assertSequenceEqual(self.imports("sample_project.a"), ["sample_project.a.a1", "sample_project.a.a2"])
        self.assertSequenceEqual(self.imports("sample_project.a.a1"), [])
        self.assertSequenceEqual(self.imports("sample_project.a.a2"), [])
        self.assertSequenceEqual(self.imports("sample_project.b"), ["sample_project.b.b1", "sample_project.b.b2"])
        self.assertSequenceEqual(self.imports("sample_project.b.b1"), ["sample_project.a"])
        self.assertSequenceEqual(self.imports("sample_project.b.b2"), ["sample_project.a"])

    def test_module_imported_by(self):
        self.assertSequenceEqual(self.imported_by("sample_project"), [])
        self.assertSequenceEqual(self.imported_by("sample_project.x"), ["sample_project"])
        self.assertSequenceEqual(self.imported_by("sample_project.a"),
                                 ["sample_project", "sample_project.b.b1", "sample_project.b.b2"])
        self.assertSequenceEqual(self.imported_by("sample_project.a.a1"), ["sample_project.a"])
        self.assertSequenceEqual(self.imported_by("sample_project.a.a2"), ["sample_project.a"])
        self.assertSequenceEqual(self.imported_by("sample_project.b"), ["sample_project.x"])
        self.assertSequenceEqual(self.imported_by("sample_project.b.b1"), ["sample_project.b"])
        self.assertSequenceEqual(self.imported_by("sample_project.b.b2"), ["sample_project.b"])

    def test_base_classes(self):
        self.assertSequenceEqual(self.base_classes("sample_project.a.a1.A1Local"), [])
        self.assertSequenceEqual(self.base_classes("sample_project.a.a1.A1Public"), [])
        self.assertSequenceEqual(self.base_classes("sample_project.a.a2.A2Local"), [])
        self.assertSequenceEqual(self.base_classes("sample_project.a.a2.A2Public"), [])
        self.assertSequenceEqual(self.base_classes("sample_project.b.b1.B1"), ["sample_project.a.a1.A1Public"])
        self.assertSequenceEqual(self.base_classes("sample_project.b.b2.B2Tool"),
                                 ["sample_project.a.a1.A1Public", "sample_project.a.a2.A2Public"])
        self.assertSequenceEqual(self.base_classes("sample_project.b.b2.B2"), ["sample_project.a.a2.A2Public"])
        self.assertSequenceEqual(self.base_classes("sample_project.x.X"), [])

    def test_descendant_classes(self):
        self.assertSequenceEqual(self.descendant_classes("sample_project.a.a1.A1Local"), [])
        self.assertSequenceEqual(self.descendant_classes("sample_project.a.a1.A1Public"), ["sample_project.b.b1.B1","sample_project.b.b2.B2Tool"])
        self.assertSequenceEqual(self.descendant_classes("sample_project.a.a2.A2Local"), [])
        self.assertSequenceEqual(self.descendant_classes("sample_project.a.a2.A2Public"), ["sample_project.b.b2.B2","sample_project.b.b2.B2Tool"])
        self.assertSequenceEqual(self.descendant_classes("sample_project.b.b1.B1"), [])
        self.assertSequenceEqual(self.descendant_classes("sample_project.b.b2.B2Tool"), [])
        self.assertSequenceEqual(self.descendant_classes("sample_project.b.b2.B2"), [])
        self.assertSequenceEqual(self.descendant_classes("sample_project.x.X"), [])
