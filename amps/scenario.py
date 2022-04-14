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
def set_for_keys(my_dict, key_arr, value):
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


def flatten_dict(my_dict):
    """Flatten a dictionary."""
    return pd.json_normalize(my_dict, sep='/').iloc[0].to_dict()


def unflatten_dict(my_dict):
    """Unflatten a dictionary."""
    result = {}
    for k,v in my_dict.items():
        set_for_keys(result, k.split('/'), v)
    return result


class ScenarioFamily:

    def __init__(self, nominal: Dict, prior: Dict):
        """Initialize a scenario family.

        Args:
            nominal (Dict): Parameters whose value is known.
            prior (Dict): Distributions of parameters in the prior.
        """
        self.flattened_nominal = flatten_dict(nominal)
        self.prior = prior

    @staticmethod
    def _get_nominal(dist):
        """Return the nominal value of a distribution."""
        # TODO (hwr26): be careful here if extending to using other dists
        if dist["scale"] == Scale.LINEAR.value:
            return dist["mu"]
        elif dist["scale"] == Scale.LOG.value:
            return np.exp(dist["mu"])
        else:
            raise ValueError(f"Unsupported scale: {dist['scale']}")

    @staticmethod
    def _get_sample(dist):
        """Return a sample from the distribution."""
        mu = dist["mu"]
        std = dist["std"]
        a, b = (dist["a"] - mu) / std, (dist["b"] - mu) / std
        val = stats.truncnorm.rvs(a,b,mu,std)
        if dist["scale"] == Scale.LINEAR.value:
            return val
        elif dist["scale"] == Scale.LOG.value:
            return np.exp(val)
        else:
            raise ValueError(f"Unsupported scale: {dist['scale']}")

    def get_nominal_scenario(self):
        """Return the nominal scenario."""
        flattened_scenario = self.flattened_nominal.copy()
        nominal = {k:self._get_nominal(v) for k,v in self.prior.items()}
        for k,v in flattened_scenario.items():
            if type(v) == str and k.split("/")[0] != "metagroup_names":
                flattened_scenario[k] = parse_expr(v, nominal)
        return unflatten_dict(flattened_scenario)

    def get_sampled_scenario(self):
        """Return a scenario sampled from the prior."""
        flattened_scenario = self.flattened_nominal.copy()
        samples = {}
        for name, dist in self.prior.items():
            samples[name] = self._get_sample(dist)
        for k,v in flattened_scenario.items():
            if type(v) == str and k.split("/")[0] != "metagroup_names":
                flattened_scenario[k] = parse_expr(v, samples)
        return unflatten_dict(flattened_scenario)