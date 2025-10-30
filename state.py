from __future__ import annotations
import random

from typing import Dict, List, Tuple
from abia_Gasolina import *
from problem_parameters import ProblemParameters


class StateRepresentation(object):
    
    def __init__(self, 
                 params: ProblemParameters, 
                 current_state: List[List[List[int]], List[int, int, Tuple,]], 
                 gasolineras: List, 
                 centros, 
                 peticiones):    
        self.current_state = current_state
        self.params = params
        self.gasolinears = gasolineras
        self.centros = centros
        self.peticiones = peticiones

    def copy(self):
        pass

    def __repr__(self) -> str:
        return f"v_c={str(self.v_c)} | {self.params}"
    
    def generate_actions(self):
        pass

    def apply_action(self):
        pass

    def heuristic(self):
        

        pass
        

#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params: ProblemParameters):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000)
    
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    gas_stations = [[None for _ in row] for row in peticiones] 
    #  Los índices de las gasolineras coinciden con los de la lista de Gasolineras 
    #  Inicialmente no hay camión que haya satisfecho las peticiones
    #  Una vez esten satisfechas se cambiará None por el índice del camión que la haya satisfecho
    
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
        CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
          
    camions = [[0, 0] for _ in centros]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion
    initial_state =  [gas_stations, camions]


    return initial_state, gasolineras_coords, centros_coords, peticiones



parametres = ProblemParameters(n_distribution_centers= random.randint(1, 10), 
                               n_gas_stations=random.randint(20, 100),
                               multiplicitat=random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0])

initial_state, gasolineras, centros, peticiones = generate_initial_state(parametres)
problem1 = StateRepresentation(initial_state, gasolineras, centros, peticiones)
print(initial_state)

for lista in initial_state:
    print(lista)