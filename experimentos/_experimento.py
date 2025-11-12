from timeit import timeit
from time import time
from aima.search import Problem, hill_climbing, simulated_annealing

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt


class Experimento:
    def __init__(self, numero_repeticiones=10):
        self.n = numero_repeticiones

        self.cache = dict()
    
    def experimento_hc(self, problem):
        print("Hill climbing")
        times_problem = list()
        values_problem = list()
        h = list()
        for i in range(self.n):
            print(f"Repeticion {i}")
            time_i = time()
            node = hill_climbing(problem)
            time_f = time()
            
            times_problem.append(time_f - time_i)
            values_problem.append((node.beneficio, node.distancia))
            h.append(node.beneficio)

        media = sum(times_problem) / len(times_problem)
        media_heuristica = sum(h) / len(h)
        times_problem.insert(0, media)
        values_problem.insert(0, media_heuristica)

        return times_problem, values_problem

    def experimento_sa(self, problem, schedule:tuple):
        print("Hill climbing")
        times_problem = list()
        values_problem = list()
        h = list()
        k, lam, limit = schedule
        for i in range(self.n):
            print(f"Repeticion {i}")
            time_i = time()
            node = simulated_annealing(problem, schedule = exp_s)
            time_f = time()
            times_problem.append(time_f - time_i)
            values_problem.append((node.beneficio, node.distancia))
            h.append(node.beneficio)


    def experimento(self, algoritmo:int=1, schedule_params:tuple=None,**versiones):
        """ 
        Algoritmo = 0 --> hill climbing
        Algoritmo = 1 --> simulated annealing
        """
        nombres = list(versiones.keys())
        problems = list(versiones.values())
        if algoritmo == 1:
            exp = self.experimento_hc
        else:
            exp = self.experimento_sa
        for i in range(len(problems)):
            print(f"---Problem {nombres[i]}---")
            resultado = exp(algoritmo = algoritmo, problem = problems[i])
            self.cache[i] = (nombres[i], resultado)
        
        return self.cache


    def get_plt(self, name:str='resultat'):
        heuristics_to_plot = list()
        times_to_plot = list()
        labels = list()
        for _, value in self.cache.items():
            labels.append(value[0])
            times_to_plot.append(value[1][0][1:])
            heuristics_to_plot.append(value[1][1][1:])

        plt.boxplot(heuristics_to_plot, tick_labels=labels)
        plt.ylabel("Valor heurístic (benefici)")
        plt.title("Comparativa d'operadors amb Boxplots")
        name += 'png'
        plt.savefig(name)
