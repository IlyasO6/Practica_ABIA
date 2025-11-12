import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))


from _experimento import Experimento
from problem_exp import GasProblem
from state_exp2 import generate_initial_state, generate_initial_state_greedy

from Practica_ABIA.problem_parameters import ProblemParameters


Exp = Experimento(numero_repeticiones=1)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)

initial_state = generate_initial_state_greedy(params=params)

problem_op1 = GasProblem(initial_state=initial_state, set_operadores=1)
problem_op2 = GasProblem(initial_state=initial_state, set_operadores=2)
problem_op3 = GasProblem(initial_state=initial_state, set_operadores=3)
problem_opx = GasProblem(initial_state=initial_state, set_operadores=0)

Exp.experimento(0, opx = problem_opx)

for i,j in Exp.cache.items():
    print(i, j, file=open("experimentos/resultados_1.txt", "a"))

#Exp.get_plt()