from typing import Generator

from aima.search import Problem


from Practica_ABIA.sets_operadores.set_operadores_1 import generate_actions_1, apply_action_1
from Practica_ABIA.sets_operadores.set_operadores_2 import generate_actions_2, apply_action_2
from Practica_ABIA.sets_operadores.set_operadores_3 import generate_actions_3, apply_action_3
from Practica_ABIA.sets_operadores.set_operadores_x import generate_actionsx, apply_actionx
class GasProblem(Problem):
    def __init__(self, initial_state, set_operadores):
        self.set_operadores = set_operadores
        if set_operadores == 1:
            self.generate = generate_actions_1
            self.apply = apply_action_1
        elif set_operadores == 2:
            self.generate = generate_actions_2
            self.apply = apply_action_2
        elif set_operadores == 3:
            self.generate = generate_actions_3
            self.apply = apply_action_3
        else:
            self.generate = generate_actionsx
            self.apply = apply_actionx


        super().__init__(initial_state)

    def actions(self, state):
        return self.generate(state)

    def result(self, state, action) :
        return self.apply(state, action)

    def value(self, state) -> float:
        distancia = state.distancia * 2
        beneficio = state.beneficio
        
        no_satisfechas = state.perdida_no_asignadas
        alpha = 1
        beta = 1
        gamma = 0.5

        #h = beneficio
        h = alpha*beneficio - distancia*beta - no_satisfechas*gamma
        #h = alpha*beneficio / (abs(no_satisfechas)*beta + abs(distancia)*gamma)
        #print(h)
        return h
        #  buscamos maximizar entonces el heurístico es (-) y el path cost (+)
        #  ambos se retornan como (-) desde state
        #  porque queremos tener poca pérdida potencial ¿no? o nos da igual
    def goal_test(self):
        return False

