import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))

from _experimento import Experimento
from problem_exp import GasProblem
from state_exp import generate_initial_state_empty, generate_initial_state_greedy, generate_initial_state_random

from Practica_ABIA.problem_parameters import ProblemParameters

Exp = Experimento(numero_repeticiones=10)

for i in range(1, 11):
    params = ProblemParameters(n_distribution_centers= 10, 
                            n_gas_stations= 100,
                            multiplicitat= 1,
                            cost_km=2*i)
    initial_state = generate_initial_state_greedy(params=params)
    problem = GasProblem(initial_state=initial_state, set_operadores=0, algoritmo=0)
    dynamic_key = f"multiplicador_coste{i}"
    kwargs = {
        dynamic_key:problem
    }
    
    Exp.experimento(algoritmo=0, **kwargs)

Exp.save_csv("resultado6.csv")
Exp.save_json_summary("resumen6.json")
#Exp.get_plt()