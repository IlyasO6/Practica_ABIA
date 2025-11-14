import sys
from pathlib import Path
from math import sqrt
from scipy.stats import ttest_ind_from_stats

ROOT = Path(__file__).resolve().parents[1]  # Practica_ABIA
sys.path.append(str(ROOT.parent))


from _experimento import Experimento
from problem_exp import GasProblem
from state_exp import generate_initial_state_empty, generate_initial_state_greedy

from Practica_ABIA.problem_parameters import ProblemParameters

n = 10
Exp = Experimento(numero_repeticiones=n)

params = ProblemParameters(n_distribution_centers= 10, 
                           n_gas_stations= 100,
                           multiplicitat= 1)

initial_state = generate_initial_state_greedy(params=params)

problem_opx = GasProblem(initial_state=initial_state, set_operadores=0, algoritmo=1)
problem_op1x = GasProblem(initial_state=initial_state, set_operadores=1, algoritmo=1)

l = ["opx", "op1x"] #  Labels 
Exp.experimento(opx = problem_opx, op1x = problem_op1x)

#  Estadísticas para la comparación de operadores
alpha = 0.05
mean_beneficio = []
std_beneficio = []
mean_distancia = []
std_distancia = []
mean_tiempo = []
std_tiempo = []
for i, j in enumerate(l):
    output = Exp.compute_summary()[j]['HC']
    #print(output)
    mean_beneficio.append(output["beneficio_mean"])
    std_beneficio.append(output["beneficio_std"])
    mean_distancia.append(output["distancia_mean"])
    std_distancia.append(output["distancia_std"])
    mean_tiempo.append(output["time_sec_mean"])
    std_tiempo.append(output["time_sec_std"])

# t-test para comparar medias (hipótesis nula: mean1 = mean2) al 95%
#  Vemos si los beneficios son iguales
t_stat_beneficio, p_value_beneficio = ttest_ind_from_stats(
    mean1=mean_beneficio[0], std1=std_beneficio[0], nobs1=n,
    mean2=mean_beneficio[1], std2=std_beneficio[1], nobs2=n,
    equal_var=False
)
test_beneficio = p_value_beneficio >= alpha # Si es False rechazamos la Null Hypothesis

#  Vemos si ambos recorren una misma cantidad de km.
t_stat_distancia, p_value_distancia = ttest_ind_from_stats(
    mean1=mean_distancia[0], std1=std_distancia[0], nobs1=n,
    mean2=mean_distancia[1], std2=std_distancia[1], nobs2=n,
    equal_var=False
)
test_distancia = p_value_distancia >= alpha # Si es False rechazamos la Null Hypothesis

#  Vemos si tardan el mismo tiempo
t_stat_tiempo, p_value_tiempo = ttest_ind_from_stats(
    mean1=mean_tiempo[0], std1=std_tiempo[0], nobs1=n,
    mean2=mean_tiempo[1], std2=std_tiempo[1], nobs2=n,
    equal_var=False
)
test_tiempo = p_value_tiempo >= alpha # Si es False rechazamos la Null Hypothesis

with open("resultados/resultado1.txt", mode = "w") as resultado:
    resultado.write(f"Resultado del T-Test del beneficio: {test_beneficio}\n \
                    Resultado del T-Test del distancia: {test_distancia}\n \
                    Resultado del T-Test del tiempo: {test_tiempo}" )
Exp.save_csv("resultado1.csv")
Exp.save_json_summary("resumen1.json")
#Exp.get_plt()
