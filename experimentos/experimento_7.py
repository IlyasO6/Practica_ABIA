import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))

from Practica_ABIA.problem_parameters import ProblemParameters
from _experimento import Experimento

km_hora = 80

Exp = Experimento(numero_repeticiones=10)

params0 = ProblemParameters(n_distribution_centers= 10, 
                        n_gas_stations= 100,
                        multiplicitat= 1)

params1 = ProblemParameters(n_distribution_centers= 10, 
                        n_gas_stations= 100,
                        multiplicitat= 1,
                        max_km=640 + km_hora)

params2 = ProblemParameters(n_distribution_centers= 10, 
                        n_gas_stations= 100,
                        multiplicitat= 1,
                        max_km=640 - km_hora)

generadores = ("greedy",)

Exp.experimento(initial_states=[generadores, "normal"], params=params0, algoritmo=0)
Exp.experimento(initial_states=[generadores, "menos_1h"], params=params1, algoritmo=0)
Exp.experimento(initial_states=[generadores, "mas_1h"], params=params2, algoritmo=0)

Exp.save_csv("resultado7.csv")
Exp.save_json_summary("resumen7.json")
#Exp.get_plt()