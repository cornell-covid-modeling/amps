import os
import amps
import yaml


RESOURCES = os.path.join(os.path.dirname(__file__), 'resources')
DETERMINISTIC = yaml.safe_load(open(f"{RESOURCES}/deterministic.yaml", "r"))
STOCHASTIC = yaml.safe_load(open(f"{RESOURCES}/stochastic.yaml", "r"))
SCENARIO_FAMILY = amps.ScenarioFamily(DETERMINISTIC, STOCHASTIC)
NOMINAL_SCENARIO = SCENARIO_FAMILY.get_nominal_scenario()
SAMPLED_SCENARIO = SCENARIO_FAMILY.get_sampled_scenario()


def test_string_parameter():
    assert NOMINAL_SCENARIO["string_parameter"] == "string"
    assert SAMPLED_SCENARIO["string_parameter"] == "string"


def test_list_parameter():
    assert NOMINAL_SCENARIO["list_parameter"] == ["item_1", "item_2", "item_3"]
    assert SAMPLED_SCENARIO["list_parameter"] == ["item_1", "item_2", "item_3"]


def test_hierarchical_parameter():
    assert NOMINAL_SCENARIO["hierarchical_parameter"]["one"]["A"] == 1
    assert NOMINAL_SCENARIO["hierarchical_parameter"]["two"]["B"] == 4
    assert SAMPLED_SCENARIO["hierarchical_parameter"]["one"]["A"] == 1
    assert SAMPLED_SCENARIO["hierarchical_parameter"]["two"]["B"] == 4


def test_relative_deterministic_parameter():
    assert NOMINAL_SCENARIO["relative_deterministic_parameter"] == 16
    assert SAMPLED_SCENARIO["relative_deterministic_parameter"] == 16


def test_relative_stochastic_parameter():
    assert NOMINAL_SCENARIO["relative_stochastic_parameter"] == 0.25
    assert SAMPLED_SCENARIO["relative_stochastic_parameter"] <= 0.5


def test_log_scale():
    assert NOMINAL_SCENARIO["log_parameter"] == 0.5
