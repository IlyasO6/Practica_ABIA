from typing import Generator

from aima.search import Problem, simulated_annealing, hill_climbing

from state import *
from operators import GasOperators

<<<<<<< HEAD
class GasProblem(Problem):
=======
class GasProblem(Problem): #mahsdgsih = 
    def __init__(self, initial_state:StateRepresentation, algoritmo:int=0):
>>>>>>> 7a14997095d907302bb9bede767f09f6a4d661b9

    def __init__(self, initial_state:StateRepresentation, algoritmo:int=0):
        """ Algoritmo: 0 --> hill climbing ; 1 --> simulated annealing """
        if algoritmo == 0:
            self.generate = initial_state.generate_actionsx
        else:
            self.generate = initial_state.generate_one_actionx

        super().__init__(initial_state)

    def actions(self, state:StateRepresentation):
        return self.generate(state)
    
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