class GasOperators(object):
    def __init__(self):
        pass

class AssignPetition(GasOperators):
    def __init__(self,
                 idx_gasolinera:int,
                 idx_peticion:int,
                 idx_camion:int,
                 idx_posicion:int,
                 diferencia_dist:float
                 ):
        self.idx_gasolinera = idx_gasolinera
        self.idx_peticion = idx_peticion
        self.idx_camion = idx_camion
        self.idx_posicion = idx_posicion
        self.diferencia_dist = diferencia_dist
    
class MovePetition(GasOperators):
    def __init__(self,
                 idx_posicion1:int,
                 idx_posicion2:int,
                 idx_camion1:int,
                 idx_camion2:int,
                 diferencia_dist1:int,
                 diferencia_dist2:int,
                 ):
        self.idx_posicion1 = idx_posicion1
        self.idx_posicion2 = idx_posicion2
        self.idx_camion1 = idx_camion1
        self.idx_camion2 = idx_camion2
        self.diferencia_dist1 = diferencia_dist1
        self.diferencia_dist2 = diferencia_dist2

class RemovePetition(GasOperators):
    def __init__(self,
                 idx_posicion:int,
                 idx_camion:int,
                 diferencia_dist:int
                 ):
        self.idx_posicion = idx_posicion
        self.idx_camion = idx_camion
        self.diferencia_dist = diferencia_dist

class IntraSwap(GasOperators):
    def __init__(self, 
                 idx_camion:int,
                 idx_posicion1:int,
                 idx_posicion2:int,
                 diferencia_dist:int
                 ):
        self.idx_camion = idx_camion
        self.idx_posicion1 = idx_posicion1
        self.idx_posicion2 = idx_posicion2
        self.diferencia_dist = diferencia_dist