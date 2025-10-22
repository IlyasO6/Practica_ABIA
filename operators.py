


class Operators(object):
    pass


class Move_to_1gas(Operators):
    def __init__(self, distr_coord, gas_coord, deposits):
        self.distr_coord = distr_coord
        self.gas_coord = gas_coord
        self.deposits = deposits

class Move_to_2gas(Operators):
    def __init__(self, distr_coord, gas1_coord, gas2_coord):
        self.distr_coord = distr_coord
        self.gas1_coord = gas1_coord
        self.gas2_coord = gas2_coord

