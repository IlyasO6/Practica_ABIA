import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))

from Practica_ABIA.problem_parameters import ProblemParameters
from _experimento import Experimento



Exp = Experimento(numero_repeticiones=10)

params1 = ProblemParameters(n_distribution_centers= 10, 
                        n_gas_stations= 100,
                        multiplicitat= 1)

params2 = ProblemParameters(n_distribution_centers= 5, 
                        n_gas_stations= 100,
                        multiplicitat= 2)

generadores = ("greedy",)

Exp.experimento(initial_states=[generadores, "multiplicitat_1"], params=params1, algoritmo=0)
Exp.experimento(initial_states=[generadores, "multiplicitat_2"], params=params2, algoritmo=0)

Exp.save_csv("resultado5.csv")
Exp.save_json_summary("resumen5.json")
#Exp.get_plt()