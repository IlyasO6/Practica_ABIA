from typing import Generator

from aima.search import Problem, hill_climbing

from abia_Gasolina import *
from state import StateRepresentation, generate_initial_state, generate_initial_state_greedy
from problem_parameters import ProblemParameters
from operators import Operators


class GasProblem(Problem):
    def __init__(self, initial_state: StateRepresentation):
        super().__init__(initial_state)

    
    def actions(self, state: StateRepresentation) -> Generator[Operators, None, None]:
        return state.generate_actions()

    def result(self, state: StateRepresentation, action: Operators) -> StateRepresentation:
        return state.apply_action(action)

    def value(self, state: StateRepresentation) -> float:
        return state.heuristic() - state.path_cost()
        #  buscamos minimizar entonces el heurístico es (-) y el path cost (+)
        #  ambos se retornan como (-) desde state
        #  porque queremos tener poca pérdida potencial ¿no? o nos da igual
    def goal_test(self):
        return False


if __name__ == "__main__":
    parametres = ProblemParameters(n_distribution_centers= random.randint(1, 10), 
                               n_gas_stations=random.randint(20, 100),
                               multiplicitat=random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0])

    initial_state = generate_initial_state_greedy(parametres)

    problem = GasProblem(initial_state)

    node = hill_climbing(problem)
    
    print(node, file=open("resultado.txt", "w"))