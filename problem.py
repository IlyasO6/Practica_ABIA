# from typing import Generator

from aima.search import Problem

from abia_Gasolina import *
from state import StateRepresentation
from problem_parameters import ProblemParameters


class GasProblem(Problem):
    def __init__(self, initial_state):
        super.__init__(initial_state)
    
    def actions(self):
        pass

    def result(self):
        pass

    def value(self):
        pass

    def goal_test(self):
        return False

