
The "Instability" and "Abstractness" metrics are related to the "Stable Dependencies Principle" and the "Stable Abstractions Principle".
This software is attempt to compute these metrics, or something equivalent, in a Python environment.
 
This distribution package installs the ``module_coupling_metrics`` command to be used from the command line.
It takes a single parameter as input -the path to the root Python package- and produces two files :
- A CSV report, one row per module
- A PNG showing the Abstractness/Instability graph for the analyzed modules

### Components

The SDP and SAP are two principles among the six "Component principles" of the Clean Architecture - even though [they existed long before this name](https://fi.ort.edu.uy/innovaportal/file/2032/1/design_principles.pdf)

These principles are not bound to any software platform.
A major difficulty is, being given a software platform, to decide what should be labeled as a "Component".
In Python, there are at least three candidates :
- [Module](https://packaging.python.org/glossary/#term-Module)
- [Import Package](https://packaging.python.org/glossary/#term-Import-Package)
- [Distribution Package](https://packaging.python.org/glossary/#term-distribution-package)

The good choice probably depends on the context:
- Analyzing a big system including all its dependencies or an independent part of it.
- The code breakdown: one class per module or many classes in each module
- ...

In this software, we use: 1 component = 1 module

### Instability

In the SDP, Instability is defined as following:
- Fan-in: Incoming dependencies. This metric identifies the number of classes outside this component that depend on classes within the component.
- Fan-out: Outgoing dependencies. This metric identifies the number of classes
inside this component that depend on classes outside the component.
- I: Instability: I = Fan-out , (Fan-in + Fan-out). This metric has the range
[0, 1]. I = 0 indicates a maximally stable component. I = 1 indicates a
maximally unstable component.

The dependencies between classes being somewhat difficult to count, we will use the following alternative :
- Fan-in: Number of modules importing the considered module.
- Fan-out: Number of modules imported by the considered module.

### Abstractness

In the SAP, Abstractness is defined as following:
- Nc: The number of classes in the component.
- Na: The number of abstract classes and interfaces in the component.
- A: Abstractness. A = Na / Nc.

The number of classes is the easy part.
The number of interfaces / abstract classes is rather tricky.

Abstract classes can be explicitly defined in Python using the abc module.
In a software where those abstract classes are systematically used, their number shall be used.
Targeting a broader context, we will consider all classes that are inherited by some other class as Abstract Classes.

Due to duck typing capabilities, interfaces are virtually non-existent in Python.
Their number is difficult to guess if they are not impersonated by a class acting as an "informal interface".
The software does nothing in this area and expects all interfaces being represented by a base class.
