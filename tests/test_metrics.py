from unittest import TestCase

from src.module_coupling_metrics.metrics import compute, Component
from src.module_coupling_metrics.project_structure import Project, Module, Class


class TestMetrics(TestCase):
    def test_compute(self):
        project = Project("p", [
            Module("m1", [Class("A"), Class("B")]),
            Module("m2", [Class("C"), Class("D")]),
            Module("m3", [Class("E"), Class("F")])
        ])
        project.gather_all_classes()
        c = lambda n: project.all_classes[n]
        c("C").base_classes = [c("A")]
        c("D").base_classes = [c("B")]
        c("E").base_classes = [c("B"), c("C")]
        c("F").base_classes = [c("D"), c("E")]
        project.compute_descendant_classes()
        m = lambda n: project.modules[n]
        m("m1").imports = []
        m("m2").imports = [m("m1")]
        m("m3").imports = [m("m1"), m("m2")]
        m("m1").imported_by = [m("m2"), m("m3")]
        m("m2").imported_by = [m("m3")]
        m("m3").imported_by = []
        components = compute(project)
        areEqual = lambda m, c: self.assertEqual(components[m].__dict__, c.__dict__)
        areEqual("m1", Component(0.0, 1.0))
        areEqual("m2", Component(0.5, 1.0))
        areEqual("m3", Component(1.0, 0.5))

    def test_empty_module(self):
        project = Project("p", [Module("m1", [])])
        components = compute(project)
        areEqual = lambda m, c: self.assertEqual(components[m].__dict__, c.__dict__)
        areEqual("m1", Component(0.0, 0.0))
