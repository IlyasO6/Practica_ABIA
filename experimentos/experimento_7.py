import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))


from _experimento import Experimento
from problem_exp import GasProblem
from state_exp import generate_initial_state, generate_initial_state_greedy

from Practica_ABIA.problem_parameters import ProblemParameters


Exp = Experimento(numero_repeticiones=1)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)

initial_state_x = generate_initial_state_greedy(params=params)

problem_opx = GasProblem(initial_state=initial_state_x, set_operadores=0, algoritmo=2)

Exp.experimento(algoritmo=2, opx = problem_opx)

for i,j in Exp.cache.items():
    print(i, j, file=open("experimentos/resultados_1.txt", "a"))

#Exp.get_plt()