from typing import Dict, List, Tuple


class Operators(object):
    def __init__(self):
        pass


class MovePeticion(Operators):
    def __init__(self, camion_origen:int, viaje_origen:int, pos_origen:int, 
                        camion_destino:int, viaje_destino:int, 
                        distancia_reducida:float, distancia_adicional:float):
        self.camion_origen = camion_origen
        self.viaje_origen = viaje_origen
        self.pos_origen = pos_origen
        self.camion_destino = camion_destino
        self.viaje_destino = viaje_destino
        self.distancia_reducida = distancia_reducida
        self.distancia_adicional = distancia_adicional

    def __repr__(self) -> str:
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

class InsertViaje(Operators):
    def __init__(self, id_camion: int, id_gasolinera: int, id_peticion: int, distancia_adicional: float):
        self.id_camion = id_camion
        self.id_gasolinera = id_gasolinera
        self.id_peticion = id_peticion
        self.distancia_adicional = distancia_adicional

    def __repr__(self) -> str:
        pass

class FillViaje(Operators):
    def __init__(self, id_camion: int, id_gasolinera: int, id_viaje: int, id_peticion: int, distancia_adicional: float):
        self.id_camion = id_camion
        self.id_gasolinera = id_gasolinera
        self.id_viaje = id_viaje
        self.id_peticion = id_peticion
        self.distancia_adicional = distancia_adicional

    def __repr__(self) -> str:
        pass

"""
class AddOnlyTrip(Operators):
    def __init__(self, gasolinera, peticio, camio, km): #los índices referenciando cada uno
        self.gasolinera = gasolinera
        self.peticio = peticio
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix petició {self.peticio} de la benzinera {self.gasolinera} i torna al centre de distribució."

class AddMultipleTrip(Operators):
    def __init__(self, gasolinera1, gasolinera2, peticio1, peticio2, camio, km):
        self.gasolinera1 = gasolinera1
        self.peticio1 = peticio1
        self.gasolinera2 =  gasolinera2
        self.peticio2 = peticio2
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."

class RemoveTrip(Operators):
    def __init__(self, camio, trip: Tuple[Tuple, Tuple], gasolinera1, peticio1, gasolinera2=None, peticio2=None, km): #  trip es la tupla que té 
        self.camio = camio
        self.trip = trip
        self.km = km
        if gasolinera2==None and peticio2==None:
            self.gasolinera = gasolinera1
            self.peticio = peticio1
        else:
            self.gasolinera1 = gasolinera1
            self.peticio1 = peticio1
            self.gasolinera2 = gasolinera2
            self.peticio2 = peticio1

    def __repr__(self) -> str:
        if self.gasolinera2==None and self.peticio2==None:
            return f"Eliminem l'assoliment de la petició {self.peticio} de la benzinera {self.gasolinera}"
        else:
            return f"Eliminem l'assoliment de les peticions: {self.peticio1} de la benzinera {self.gasolinera1} i {self.peticio2} de la benzinera {self.gasolinera2}"
        
            
        
class InterchangeTrips(Operators):
    def __init__(self, camio1, 
                 trip1: Tuple[Tuple, Tuple], 
                 gasolinera1_1, 
                 gasolinera1_2=None, 
                 peticio1_1, 
                 peticio1_2=None, 
                 camio2, 
                 trip2: Tuple[Tuple, Tuple], 
                 gasolinera2_1, 
                 gasolinera2_2=None, 
                 peticio2_1, 
                 peticio2_2=None): #  trip es la tupla que té 
        self.camio1 = camio1
        self.trip1 = trip1
        if gasolinera1_2 == None:
            self.gasolinera1 = gasolinera1_1
            self.peticio1 = peticio1_1
        else:
            self.gasolinera1_1 = gasolinera1_1
            self.peticio1_1 = peticio1_1
            self.gasolinera1_2 = gasolinera1_2
            self.peticio1_2 = peticio1_2

        self.camio2 = camio2
        self.trip2 = trip2
        if gasolinera2_2 == None:
            self.gasolinera2 = self.gasolinera2_1
            self.peticio2 = self.peticio2_1
        else:
            self.gasolinera2_1 = gasolinera2_1
            self.peticio2_1 = peticio2_1
            self.gasolinera2_2 = gasolinera2_2
            self.peticio2_2 = peticio2_2

    def __repr__(self) -> str:
            return f"Intercambiem els viatges {self.trip1} i {self.trip2} de camio {self.camio1} i {self.camio2}"
"""

"""
    # AddOnlyTrip
    for gasolinera in range(len(self.current_state[0])):
        for peticio in range(len(self.current_state[0][gasolinera])):
            if self.current_state[0][gasolinera][peticio] == None:
                for camio in range(len(self.current_state[1])):
                    x1, y1 = self.gasolineras[gasolinera]
                    x2, y2 = self.centros[camio]
                    distancia = abs(x2-x1)+abs(y2-y1)
                    km = 2*distancia
                    if self.current_state[1][camio][0]+km < 640 and len(self.current_state[1][camio])<7:
                        yield AddOnlyTrip(gasolinera, peticio, camio, km)
    # AddMultipleTrip
                for gasolinera2 in range(len(self.current_state[0])):
                    for peticio2 in range(len(self.current_state[0][gasolinera2])):
                        if self.current_state[0][gasolinera2][peticio2] == None:
                            for camio in range(len(self.current_state[1])):
                                x1, y1 = self.gasolineras[gasolinera]
                                x2, y2 = self.centros[camio]
                                x3, y3 = self.gasolineras[gasolinera2]
                                distancia1 = abs(x2-x1)+abs(y2-y1)
                                distancia2 = abs(x3-x1)+abs(y3-y1)
                                distancia3 = abs(x3-x2)+abs(y3-y2)
                                km = distancia1+distancia2+distancia3
                                if self.current_state[1][camio][0]+km < 640 and len(self.current_state[1][camio])<7:
                                    yield AddMultipleTrip(gasolinera, gasolinera2, peticio, peticio2, camio, km)
    # RemoveTrip
    for camio in range(len(self.current_state[1])):
        if len(self.current_state[1][camio]) > 1: # mirem si el camio té algun viatge
            for tuple in range(1, len(self.current_state[1][camio]+1)):
                trip = self.current_state[1][camio][tuple]
                if len(tuple) == 1:
                    gasolinera = trip[0][0]
                    peticio = trip[0][1]
                    x1, y1 = self.gasolineras[gasolinera]
                    x2, y2 = self.centros[camio]
                    distancia = abs(x2-x1)+abs(y2-y1)
                    km = 2*distancia
                    yield RemoveTrip(camio, trip, gasolinera, peticio, km)
                else:
                    gasolinera = trip[0][0]
                    peticio = trip[0][1]
                    gasolinera2 = trip[1][0]
                    peticio2 = trip[1][1]
                    x1, y1 = self.gasolineras[gasolinera]
                    x2, y2 = self.centros[camio]
                    x3, y3 = self.gasolineras[gasolinera2]
                    distancia1 = abs(x2-x1)+abs(y2-y1)
                    distancia2 = abs(x3-x1)+abs(y3-y1)
                    distancia3 = abs(x3-x2)+abs(y3-y2)
                    km = distancia1+distancia2+distancia3
                    yield RemoveTrip(camio, trip, gasolinera, peticio, gasolinera2, peticio2, km)

    # InterchangeTrips
                for camio2 in range(len(self.current_state[1])):
                    if len(self.current_state[1][camio2]) > 1: # mirem si el camio té algun viatge
                        for tuple in range(1, len(self.current_state[1][camio2]+1)):
                            trip2 = self.current_state[1][camio2][tuple]
                            if len(trip) == 1:
                                gasolinera = trip[0][0]
                                peticio = trip[0][1]
                                x1, y1 = self.gasolineras[gasolinera]
                                x2, y2 = self.centros[camio]
                                distancia = abs(x2-x1)+abs(y2-y1)
                                km1 = 2*distancia
                            else:
                                gasolinera1_1 = trip[0][0]
                                peticio1_1 = trip[0][1]
                                gasolinera1_2 = trip[1][0]
                                peticio1_2 = trip[1][1]
                                x1, y1 = self.gasolineras[gasolinera1_1]
                                x2, y2 = self.centros[camio]
                                x3, y3 = self.gasolineras[gasolinera1_2]
                                distancia1 = abs(x2-x1)+abs(y2-y1)
                                distancia2 = abs(x3-x1)+abs(y3-y1)
                                distancia3 = abs(x3-x2)+abs(y3-y2)
                                km1 = distancia1+distancia2+distancia3
                            
                            if len(trip2) == 1:
                                gasolinera2 = trip2[0][0]
                                peticio2 = trip2[0][1]
                                x1, y1 = self.gasolineras[gasolinera2]
                                x2, y2 = self.centros[camio2]
                                distancia = abs(x2-x1)+abs(y2-y1)
                                km2 = 2*distancia
                                if gasolinera:
                                    yield InterchangeTrips(camio, trip, gasolinera, peticio, camio2, gasolinera2, peticio2)
                                else:
                                    yield InterchangeTrips(camio, trip, gasolinera1_1, gasolinera1_2, peticio1_1, peticio1_2, camio2, gasolinera2, peticio2)
                            else:
                                gasolinera2_1 = trip[0][0]
                                peticio2_1 = trip[0][1]
                                gasolinera2_2 = trip[1][0]
                                peticio2_2 = trip[1][1]
                                x1, y1 = self.gasolineras[gasolinera2_1]
                                x2, y2 = self.centros[camio2]
                                x3, y3 = self.gasolineras[gasolinera2_2]
                                distancia1 = abs(x2-x1)+abs(y2-y1)
                                distancia2 = abs(x3-x1)+abs(y3-y1)
                                distancia3 = abs(x3-x2)+abs(y3-y2)
                                km2 = distancia1+distancia2+distancia3
                                if gasolinera:
                                    yield InterchangeTrips(camio, trip, gasolinera, peticio, camio2, gasolinera2_1, gasolinera2_2, peticio2_1, peticio2_2)
                                else:
                                    yield InterchangeTrips(camio, trip, gasolinera1_1, gasolinera1_2, peticio1_1, peticio1_2, camio2, gasolinera2_2, peticio2_1, peticio2_1, peticio2_1)             
"""