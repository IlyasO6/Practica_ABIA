import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))


from _experimento import Experimento
from problem_exp import GasProblem
from state_exp import generate_initial_state_empty, generate_initial_state_greedy, generate_initial_state_random

from Practica_ABIA.problem_parameters import ProblemParameters


Exp = Experimento(numero_repeticiones=10)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)
initial_state = generate_initial_state_greedy(params=params)
"""
lim = 10000

schedules = [
    (10, 0.001, lim),
    (50, 0.01, lim),
]

K = (10, 20, 50, 100, 500, 1000, 5000, 50000)
LAM = (0.0001, 0.0005, 0.001, 0.01, 0.1)
'''
K2 = (10, 50, 500, 5000)
LAM2 = (0.0001, 0.001, 0.01, 0.1)
for k in K2:
    for lam in LAM2:
        schedules.append((k, lam, 10000))
'''

traces = []
i = 1
for (k, lam, limit) in schedules:
    print("Conjunto", i, ":", f"({k}, {lam}, {limit})")

    out = Exp.sa_run_with_trace(problem, schedule_params=(k,lam,limit), label=f"k={k}, λ={lam}, L={limit}")
    traces.append(out)
    i += 1

png = Exp.plot_sa_trace_beneficio_coste(traces, filename="sa_trace_beneficio_coste2(for_k_lam)7.png")
print("Saved", png)
"""
K = (5, 20, 50)
LAM = (0.001, 0.0005, 0.0001)
generadores = ("greedy",)
i = 0
for k in K:
    for lam in LAM:
        pass
#Exp.experimento(algoritmo=1, schedule_params=(8.4, 0.2221, 1000), sa0 = problem_sa)
#Exp.experimento(algoritmo=1, schedule_params=(5, 0.1, 1000), sa1 = problem_sa)
#  cogemos este: --> Exp.experimento(algoritmo=1, schedule_params=(10, 0.5, 1000), sa2 = problem_sa)

Exp.experimento(algoritmo=1, schedule_params=(5, 0.001, 2000), initial_states=[generadores, f"sa_L-{0.001}--K-{5}"], params = params)
        

#Exp.experimento(algoritmo=0, initial_states=[generadores, "hc"], params = params)

#Exp.experimento(algoritmo=0, hc=problem_hc)
"k_50--lam_0.0005"
#Exp.experimento(algoritmo=1, schedule_params=None, opx = problem)

#Exp.save_csv("resultado3.csv")
Exp.save_json_summary("resumen3.json")
#Exp.get_plt()
"""
good:

(5, 0.001, 1000)
k_20--lam_0.5
k_10--lam_0.0005
k_10--lam_0.1
k_1--lam_0.01
k_1--lam_0.5
"""