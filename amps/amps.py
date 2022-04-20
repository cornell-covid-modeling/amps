import numpy as np
import pandas as pd
import scipy.stats as stats
from sympy.parsing.sympy_parser import parse_expr
from enum import Enum
from typing import Dict


class Scale(Enum):
    LINEAR = "linear"
    LOG = "log"


# https://stackoverflow.com/a/54829922
def _set_for_keys(my_dict, key_arr, value):
    """Set value at path in my_dict defined by key array."""
    current = my_dict
    for i in range(len(key_arr)):
        key = key_arr[i]
        if key not in current:
            if i == len(key_arr)-1:
                current[key] = value
            else:
                current[key] = {}
        else:
            if type(current[key]) is not dict:
                raise ValueError("Dictionary key already occupied")
        current = current[key]
    return my_dict


def _flatten_dict(my_dict):
    """Flatten a dictionary."""
    return pd.json_normalize(my_dict, sep='/').iloc[0].to_dict()


def _un_flatten_dict(my_dict):
    """Unflatten a dictionary."""
    result = {}
    for k,v in my_dict.items():
        _set_for_keys(result, k.split('/'), v)
    return result


def _scale_val(val, scale):
    """Scale the given value by the given scale."""
    if scale == Scale.LINEAR.value:
        return val
    elif scale == Scale.LOG.value:
        return np.exp(val)
    else:
        raise ValueError(f"Unsupported scale: {scale}")


def _get_nominal(dist):
    """Return the nominal value of a distribution."""
    return _scale_val(dist["mu"], dist["scale"])


def _get_sample(dist):
    """Return a sample from the distribution."""
    mu = dist["mu"]
    std = dist["std"]
    a, b = (dist["a"] - mu) / std, (dist["b"] - mu) / std
    val = stats.truncnorm.rvs(a,b,mu,std)
    return _scale_val(val, dist["scale"])


class ScenarioFamily:

    def __init__(self, deterministic: Dict, stochastic: Dict):
        """Initialize a scenario family.

        Args:
            deterministic (Dict): Parameters whose value is known explicitly.
            stochastic (Dict): Parameters to be drawn from a distribution.
        """
        self.flattened_deterministic = _flatten_dict(deterministic)
        self.stochastic = stochastic

    def get_nominal_scenario(self):
        """Return the nominal scenario."""
        flattened_scenario = self.flattened_deterministic.copy()
        nominal = {k:_get_nominal(v) for k,v in self.stochastic.items()}
        flattened_scenario.update(nominal)
        for k,v in flattened_scenario.items():
            if type(v) == str and v[:6] == "parse:" and k.split("/")[0]:
                flattened_scenario[k] = parse_expr(v[7:], flattened_scenario)
        return _un_flatten_dict(flattened_scenario)

    def get_sampled_scenario(self):
        """Return a scenario sampled from the stochastic."""
        flattened_scenario = self.flattened_deterministic.copy()
        samples = {}
        for name, dist in self.stochastic.items():
            samples[name] = _get_sample(dist)
        flattened_scenario.update(samples)
        for k,v in flattened_scenario.items():
            if type(v) == str and v[:6] == "parse:" and k.split("/")[0]:
                flattened_scenario[k] = parse_expr(v[7:], flattened_scenario)
        return _un_flatten_dict(flattened_scenario)
