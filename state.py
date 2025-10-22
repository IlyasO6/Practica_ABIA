from __future__ import annotations
import random

from typing import Dict
from abia_Gasolina import *
from problem_parameters import ProblemParameters


class StateRepresentation(object):
    
    def __init__(self, params: ProblemParameters, state: list[tuple[int,]], gas):
        self.current_state = state
        self.params = params


#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params: ProblemParameters):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat




parametres = ProblemParameters(n_distribution_centers= random.randint(1, 10), n_gas_stations=random.randint(10))