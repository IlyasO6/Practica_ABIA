from typing import Generator

from aima.search import Problem


from Practica_ABIA.sets_operadores.set_operadores_1 import generate_actions_1, apply_action_1
from Practica_ABIA.sets_operadores.set_operadores_2 import generate_actions_2, apply_action_2
from Practica_ABIA.sets_operadores.set_operadores_3 import generate_actions_3, apply_action_3

class GasProblem(Problem):
    def __init__(self, initial_state, set_operadores):

        if set_operadores == 1:
            self.generate = generate_actions_1
            self.apply = apply_action_1
        elif set_operadores == 2:
            self.generate = generate_actions_2
            self.apply = apply_action_2
        else:
            self.generate = generate_actions_3
            self.apply = apply_action_3


        super().__init__(initial_state)

    
    def actions(self, state):
        return self.generate(state)

    def result(self, state, action) :
        return self.apply(state, action)

    def value(self, state) -> float:
        beneficio = state.heuristic()
        no_satisfechas, distancia = state.path_cost()
        alpha = 1
        beta = 0.2
        gamma = 1

        #h = beneficio
        h = alpha*beneficio - distancia*gamma
        #h = alpha*beneficio / (abs(no_satisfechas)*beta + abs(distancia)*gamma)

        return h
        #  buscamos maximizar entonces el heurístico es (-) y el path cost (+)
        #  ambos se retornan como (-) desde state
        #  porque queremos tener poca pérdida potencial ¿no? o nos da igual
    def goal_test(self):
        return False

