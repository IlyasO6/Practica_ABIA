from typing import Generator

from aima.search import Problem

from state import StateRepresentation
from operators import GasOperators

class GasProblem(Problem):
    def __init__(self, initial_state:StateRepresentation, algoritmo:int=0):

        if algoritmo == 0:
            self.generate = initial_state.generate_actionsx
        else:
            self.generate = initial_state.generate_one_actionx

        super().__init__(initial_state)

    def actions(self, state:StateRepresentation):
        return self.generate(state)

    def result(self, state:StateRepresentation, action:Generator[GasOperators, 0, 0]):
        return state.apply(action)

    def value(self, state) -> float:
        distancia = state.distancia * state.COST_KM
        beneficio = state.beneficio
        no_satisfechas = state.perdida_no_asignadas
        alpha = 1
        beta = 1
        gamma = 0.5
        
        h = alpha*beneficio - (distancia*beta + no_satisfechas*gamma)

        return h
    
    def goal_test(self):
        return False

