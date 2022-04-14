"""
amps
====

amps offers a maintainable parameter management system for applications
requiring both deterministic and non-stochastic parameters. It is compatible
with hierarchical parameter structures specified in either YAML or JSON format.
Furthermore, parameters can be defined as the (simple) function of other
parameters within YAML/JSON files reducing coupling and increasing readability.
"""

__author__ = "Cornell Covid Modeling Team"

from .scenario import ScenarioFamily
