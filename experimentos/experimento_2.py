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

initial_state = generate_initial_state(params=params)
initial_state_greedy = generate_initial_state_greedy(params=params)

problem_empty = GasProblem(initial_state=initial_state, set_operadores=0, algoritmo=1)
problem_greedy = GasProblem(initial_state=initial_state_greedy, set_operadores=1, algoritmo=1)

Exp.experimento(empty = problem_empty, greedy = problem_greedy)
Exp.save_csv("resultado1.csv")
Exp.save_json_summary("resumen1.json")
#Exp.get_plt()