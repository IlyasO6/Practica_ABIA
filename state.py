from __future__ import annotations
import random

from typing import Dict, List, Tuple
from abia_Gasolina import *
from problem_parameters import ProblemParameters


class StateRepresentation(object):
    
    def __init__(self, params: ProblemParameters, state: List[List[Tuple,], List[int,]], gasolineras, centros):
        self.current_state = state
        self.params = params



#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params: ProblemParameters):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000)
    
    centros = CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    initial_state = [((gasolinera.cx, gasolinera.cy), None, None) for gasolinera in gasolineras]
    
    return initial_state



parametres = ProblemParameters(n_distribution_centers= random.randint(1, 10), 
                               n_gas_stations=random.randint(20, 100),
                               multiplicitat=random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0])

initial_state = generate_initial_state(parametres)

for gas in initial_state:
    print(gas)