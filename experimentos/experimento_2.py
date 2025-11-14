import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))

from Practica_ABIA.problem_parameters import ProblemParameters
from _experimento import Experimento



Exp = Experimento(numero_repeticiones=10)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)

generadores = ("greedy", "empty", "random")

Exp.experimento(initial_states=generadores, params=params)
Exp.save_csv("resultado2.csv")
Exp.save_json_summary("resumen2.json")
#Exp.get_plt()