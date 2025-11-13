import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))


from _experimento import Experimento
from problem_exp import GasProblem
from state_exp import generate_initial_state, generate_initial_state_greedy

from Practica_ABIA.problem_parameters import ProblemParameters


Exp = Experimento(numero_repeticiones=10)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)

initial_state = generate_initial_state_greedy(params=params)

problem_opx = GasProblem(initial_state=initial_state, set_operadores=0, algoritmo=1)
problem_op1x = GasProblem(initial_state=initial_state, set_operadores=1, algoritmo=1)

Exp.experimento(opx = problem_opx, op1x = problem_op1x)
Exp.save_csv("resultado1.csv")
Exp.save_json_summary("resumen1.json")
#Exp.get_plt()