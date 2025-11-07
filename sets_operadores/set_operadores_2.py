

#  Operadores 2
class Operators(object):
    def __init__(self):
        pass

class SwapPeticiones(Operators):
    def __init__(self, id_camion_1: int, id_viaje_1: int, pos_1: int,
                        id_camion_2: int, id_viaje_2: int, pos_2: int, 
                        delta_camion1: float, delta_camion2: float):
        self.id_camion_1 = id_camion_1
        self.id_viaje_1 = id_viaje_1
        self.pos_1 = pos_1
        self.id_camion_2 = id_camion_2
        self.id_viaje_2 = id_viaje_2
        self.pos_2 = pos_2
        self.delta_camion1 = delta_camion1
        self.delta_camion2 = delta_camion2

    def __repr__(self) -> str:
        pass

class RemovePeticion(Operators):
    def __init__(self, id_camion: int, id_viaje: int, id_peticion: int, distancia_reducida: float):
        self.id_camion = id_camion
        self.id_viaje = id_viaje
        self.id_peticion = id_peticion
        self.distancia_reducida = distancia_reducida

    def __repr__(self) -> str:
        pass

class AddPeticion(Operators):
    def __init__(self, id_camion: int, id_gasolinera: int, id_peticion: int, distancia_adicional: float, id_trip = None):
        self.id_camion = id_camion
        self.id_trip = id_trip
        self.id_gasolinera = id_gasolinera
        self.id_peticion = id_peticion
        self.distancia_adicional = distancia_adicional

    def __repr__(self) -> str:
        pass

# Generate actions