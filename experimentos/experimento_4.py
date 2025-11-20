import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))

from Practica_ABIA.problem_parameters import ProblemParameters
from _experimento import Experimento



Exp = Experimento(numero_repeticiones=10)

base = (10, 100)

for i in range(1, 5):
    params = ProblemParameters(n_distribution_centers= 10*i, 
                            n_gas_stations= 100*i,
                            multiplicitat= 1)

    generadores = ("greedy",)

    Exp.experimento(initial_states=[generadores, f"multiplicador_{i}"], schedule_params=(5, 0.001, 5000), params=params, algoritmo=1, multiplicador=i)

Exp.save_csv("resultado4.csv")
Exp.save_json_summary("resumen4.json")
#Exp.get_plt()