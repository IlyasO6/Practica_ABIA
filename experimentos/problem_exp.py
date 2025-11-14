from typing import Generator

from aima.search import Problem


from Practica_ABIA.sets_operadores.set_operadores_1 import generate_actions_1, apply_action_1
from Practica_ABIA.sets_operadores.set_operadores_2 import generate_actions_2, apply_action_2
from Practica_ABIA.sets_operadores.set_operadores_3 import generate_actions_3, apply_action_3
from Practica_ABIA.sets_operadores.set_operadores_x import generate_actionsx, apply_actionx, generate_one_actionx
from Practica_ABIA.sets_operadores.set_operadores_1x import generate_actions1x, apply_action1x, generate_one_action1x
class GasProblem(Problem):
    def __init__(self, initial_state, set_operadores, algoritmo:int=0):
        self.set_operadores = set_operadores
        if set_operadores == 1:
            if algoritmo == 0:
                self.generate = generate_actions1x
            else:
                self.generate = generate_one_action1x
            self.apply = apply_action1x
        elif set_operadores == 2:
            self.generate = generate_actions_2
            self.apply = apply_action_2
        elif set_operadores == 3:
            self.generate = generate_actions_3
            self.apply = apply_action_3
        else:
            if algoritmo == 0:
                self.generate = generate_actionsx
            else:
                self.generate = generate_one_actionx
            self.apply = apply_actionx

        super().__init__(initial_state)

    def actions(self, state):
        return self.generate(state)

    def result(self, state, action) :
        new_state = self.apply(state, action)
        new_state.pasos += 1
        if not hasattr(new_state, "sa_trace") or new_state.sa_trace is None:
            new_state.sa_trace = [(float(state.beneficio), float(state.distancia + state.perdida_no_asignadas))]
        new_state.sa_trace.append(
            (float(new_state.beneficio), float(new_state.distancia + new_state.perdida_no_asignadas))
        )
        return new_state

    def value(self, state) -> float:
        distancia = state.distancia * state.COST_KM
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

