# Amps Manages ParameterS

[![CircleCI](https://circleci.com/gh/cornell-covid-modeling/amps/tree/master.svg?style=shield&circle-token=185a488c312ed92d2a98ed28060f8c985ec6b57e)](https://circleci.com/gh/cornell-covid-modeling/amps/tree/master)
[![codecov](https://codecov.io/gh/cornell-covid-modeling/amps/branch/master/graph/badge.svg?token=QMJ2E54YPL)](https://codecov.io/gh/cornell-covid-modeling/amps)

amps offers a maintainable parameter management system for applications
requiring both deterministic and non-stochastic parameters. It is compatible
with hierarchical parameter structures specified in either YAML or JSON format.
Furthermore, parameters can be defined as the (simple) function of other
parameters within YAML/JSON files reducing coupling and increasing readability.
