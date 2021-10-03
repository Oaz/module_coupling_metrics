"""A wrapper around multiple module inspection tools to collect project structure data."""

import importlib
import inspect
import sys

from pydeps import cli
from pydeps.py2depgraph import py2dep
from pydeps.target import Target
from .project_structure import Project, Module, Class


def load_project_structure(top_level_path):
    def full_class_name(info):
        return info.__module__ + '.' + info.__name__

    def sort_by_name(l):
        return sorted(l, key=lambda x: x.name)

    def create_class(info):
        cls = Class(full_class_name(info))
        cls.hierarchy = inspect.getmro(info)
        return cls.name, cls

    def create_module(info):
        module = Module(info.name)
        module.info = info
        try:
            spec = importlib.util.spec_from_file_location(info.name, info.path)
            if info.name in sys.modules:
                m = sys.modules[info.name]
            else:
                m = importlib.util.module_from_spec(spec)
                sys.modules[info.name] = m
                spec.loader.exec_module(m)
            referenced_classes = inspect.getmembers(m, inspect.isclass)
            module.classes = dict([create_class(cls) for (_, cls) in referenced_classes if cls.__module__ == info.name])
        except Exception as err:
            sys.stderr.write("%s> %s\n" % (info.name, err.args[0]))
        return module.name, module

    target = Target(top_level_path)
    project = Project(target.modname)
    has_interest_in = lambda n: (n+'.').startswith(project.name+'.')
    cli.verbose = cli._not_verbose
    py2dep_args = dict()
    py2dep_args['exclude_exact'] = []
    py2dep_args['show_cycles'] = False
    py2dep_args['show_raw_deps'] = False
    py2dep_args['noise_level'] = 100
    py2dep_args['max_bacon'] = 100
    py2dep_args['show_deps'] = True
    deps = py2dep(target, **py2dep_args)
    dependencies_between_modules = deps.sources
    project.modules = dict([create_module(m) for (_, m) in dependencies_between_modules.items() if has_interest_in(m.name)])
    project.gather_all_classes()
    for (_, module) in project.modules.items():
        module.imports = sort_by_name([project.modules[name] for name in module.info.imports if has_interest_in(name)])
        module.imported_by = sort_by_name([project.modules[name] for name in module.info.imported_by if has_interest_in(name)])
        for (_, cls) in module.classes.items():
            base_classes_names = [full_class_name(parent) for parent in cls.hierarchy[1:] if has_interest_in(parent.__module__)]
            cls.base_classes = sort_by_name([project.all_classes[name] for name in base_classes_names if name in project.all_classes])
            del cls.hierarchy
        del module.info
    project.compute_descendant_classes()
    return project
