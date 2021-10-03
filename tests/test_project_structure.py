from unittest import TestCase
from src.module_coupling_metrics.project_structure import Project, Module, Class


class TestProject(TestCase):
    def test_gather_all_classes(self):
        expected_classes = [Class("c1a"), Class("c1b"), Class("c2a"), Class("c2b")]
        project = Project(
            "p",
            [Module("m1", expected_classes[0:2]), Module("m2", expected_classes[2:4])]
        )
        project.gather_all_classes()
        self.assertSequenceEqual(project.all_classes, dict([(x.name, x) for x in expected_classes]))

    def compute_descendant_classes(self, runs):
        project = Project("p", [Module("m1", [Class("A"), Class("B")]), Module("m2", [Class("C")])])
        project.gather_all_classes()
        c = project.all_classes
        c["B"].base_classes = [c["A"]]
        c["C"].base_classes = [c["B"], c["A"]]
        for run in range(runs):
            project.compute_descendant_classes()
        self.assertSequenceEqual(c["A"].descendant_classes, [c["B"], c["C"]])
        self.assertSequenceEqual(c["B"].descendant_classes, [c["C"]])
        self.assertSequenceEqual(c["C"].descendant_classes, [])

    def test_compute_descendant_classes(self):
        self.compute_descendant_classes(1)

    def test_compute_descendant_classes_can_be_called_multiple_times(self):
        self.compute_descendant_classes(2)
