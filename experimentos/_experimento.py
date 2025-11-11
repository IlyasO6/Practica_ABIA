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
    
    def _experimento(self, algoritmo, problem):
        if algoritmo == 0:
            func = hill_climbing
        else:
            func = simulated_annealing

        times_problem = list()
        values_problem = list()
        for i in range(self.n):
            print(f"Repeticion {i}")
            time_i = time()
            node = func(problem)
            time_f = time()
            
            times_problem.append(time_f - time_i)
            values_problem.append(node.beneficio - node.distancia*2)

        media = sum(times_problem) / len(times_problem)
        media_heuristica = sum(values_problem) / len(values_problem)
        times_problem.insert(0, media)
        values_problem.insert(0, media_heuristica)

        return times_problem, values_problem

    def experimento(self, algoritmo:int, **versiones):
        """ 
        Algoritmo = 0 --> hill climbing
        Algoritmo = 1 --> simulated annealing
        """
        nombres = list(versiones.keys())
        problems = list(versiones.values())
        for i in range(len(problems)):
            print(f"---Problem {nombres[i]}---")
            resultado = self._experimento(algoritmo = algoritmo, problem = problems[i])
            self.cache[i] = (nombres[i], resultado)


    def get_plt(self):
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
        plt.savefig('resultat.png')
