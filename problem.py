from typing import Generator

from aima.search import Problem, simulated_annealing, hill_climbing

from state import *
from operators import GasOperators

class GasProblem(Problem):

    def __init__(self, initial_state:StateRepresentation, algoritmo:int=0):
        """ Algoritmo: 0 --> hill climbing ; 1 --> simulated annealing """
        self.algoritmo = algoritmo
        super().__init__(initial_state)

    def actions(self, state:StateRepresentation):
        if self.algoritmo == 0:
            return state.generate_actionsx()
        else:
            return state.generate_one_actionx()
    
    def result(self, state:StateRepresentation, action:Generator[GasOperators, 0, 0]):
        #  state no se refiere al nombre del archivo, es un argumento del tipo StateRepresentation
        return state.apply_actionx(action)

    def value(self, state) -> float:
        """ Función heuristica """
        distancia = state.distancia * state.COST_KM #  Distancia * precio por km
        beneficio = state.beneficio #  beneficio total actual
        no_satisfechas = state.perdida_no_asignadas #  perdida por peticiones no asignadas 
        
        # ponderadores
        alpha = 1
        beta = 1
        gamma = 0.5
        
        #  funcion heurística
        h = alpha*beneficio - (distancia*beta + no_satisfechas*gamma)

        return h
    
    def goal_test(self):
        #  devolvemos False porque es busqueda local
        return False

if __name__ == '__main__':
    params = ProblemParameters(n_distribution_centers=10, 
                            n_gas_stations=100, 
                            multiplicitat=1)

    initial_state = generate_initial_state_greedy(params=params)

    problem = GasProblem(initial_state=initial_state, algoritmo=0)

    node = hill_climbing(problem)

    print(f"Beneficio: {node.beneficio}\nDistancia total: {node.distancia}\nBeneficio neto: {node.beneficio - node.distancia*2}")