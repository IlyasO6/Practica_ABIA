from __future__ import annotations
import random

from typing import Dict, List, Tuple
from operators import *
from abia_Gasolina import *
from problem_parameters import ProblemParameters


class StateRepresentation(object):
    

    def __init__(self, 
                 params: ProblemParameters, 
                 current_state: List[List[List[int]], List[int, Tuple,]], 
                 gasolineras: List, 
                 centros, 
                 peticiones):    
        self.current_state = current_state
        self.params = params
        self.gasolineras = gasolineras
        self.centros = centros
        self.peticiones = peticiones

        self.dists:list
        self.dists_gasolineras:list


    def copy(self):
        pass

    def __repr__(self) -> str:
        return f"v_c={str(self.v_c)} | {self.params}"
    
    @classmethod
    def preprocessament_distancies(cls):
        matriu_distancies = list()
        matriu_distancies_gasolineres = list()
        for gasolinera_coord in self.gasolineras:
            row = list()
            row2 = list()
            for centro_coord in self.centros:
                distancia = abs(centro_coord[0] - gasolinera_coord[0]) + abs(centro_coord[1] - gasolinera_coord[1])
                row.append(distancia)
            
            for gasolinera_coord2 in self.gasolineras:
                distancia = abs(gasolinera_coord2[0] - gasolinera_coord[0]) + abs(gasolinera_coord2[1] - gasolinera_coord[1])
                row2.append(distancia)
            
            matriu_distancies.append(row)
            matriu_distancies_gasolineres.append(row2)
        
        cls.dists = matriu_distancies
        cls.dists_gasolineras = matriu_distancies_gasolineres

    def generate_actions(self):
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
        for gasolinera1 in range(len(self.current_state[0])):
            for peticio1 in range(len(self.current_state[0][gasolinera1])):
                if self.current_state[0][gasolinera1][peticio1] == None:
                    for gasolinera2 in range(len(self.current_state[0])):
                        for peticio2 in range(len(self.current_state[0][gasolinera2])):
                            if self.current_state[0][gasolinera2][peticio2] == None:
                                for camio in range(len(self.current_state[1])):
                                    x1, y1 = self.gasolineras[gasolinera1]
                                    x2, y2 = self.centros[camio]
                                    x3, y3 = self.gasolineras[gasolinera2]
                                    distancia1 = abs(x2-x1)+abs(y2-y1)
                                    distancia2 = abs(x3-x1)+abs(y3-y1)
                                    distancia3 = abs(x3-x2)+abs(y3-y2)
                                    km = distancia1+distancia2+distancia3
                                    if self.current_state[1][camio][0]+km < 640 and len(self.current_state[1][camio])<7:
                                        yield AddMultipleTrip(gasolinera1, gasolinera2, peticio1, peticio2, camio, km)
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
                        gasolinera1 = trip[0][0]
                        peticio1 = trip[0][1]
                        gasolinera2 = trip[1][0]
                        peticio2 = trip[1][1]
                        x1, y1 = self.gasolineras[gasolinera1]
                        x2, y2 = self.centros[camio]
                        x3, y3 = self.gasolineras[gasolinera2]
                        distancia1 = abs(x2-x1)+abs(y2-y1)
                        distancia2 = abs(x3-x1)+abs(y3-y1)
                        distancia3 = abs(x3-x2)+abs(y3-y2)
                        km = distancia1+distancia2+distancia3
                        yield RemoveTrip(camio, trip, gasolinera1, peticio1, gasolinera2, peticio2, km)

        # InterchangeTrips
        for camio1 in range(len(self.current_state[1])):
            if len(self.current_state[1][camio1]) > 1: # mirem si el camio té algun viatge
                for tuple in range(1, len(self.current_state[1][camio1]+1)):
                    trip1 = self.current_state[1][camio1][tuple]
                    for camio2 in range(len(self.current_state[1])):
                        if len(self.current_state[1][camio2]) > 1: # mirem si el camio té algun viatge
                            for tuple in range(1, len(self.current_state[1][camio2]+1)):
                                trip2 = self.current_state[1][camio2][tuple]
                                if len(trip1) == 1:
                                    gasolinera1 = trip1[0][0]
                                    peticio1 = trip1[0][1]
                                    x1, y1 = self.gasolineras[gasolinera1]
                                    x2, y2 = self.centros[camio1]
                                    distancia = abs(x2-x1)+abs(y2-y1)
                                    km1 = 2*distancia
                                else:
                                    gasolinera1_1 = trip1[0][0]
                                    peticio1_1 = trip1[0][1]
                                    gasolinera1_2 = trip1[1][0]
                                    peticio1_2 = trip1[1][1]
                                    x1, y1 = self.gasolineras[gasolinera1_1]
                                    x2, y2 = self.centros[camio1]
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
                                    if gasolinera1:
                                        yield InterchangeTrips(camio1, trip1, gasolinera1, peticio1, camio2, gasolinera2, peticio2)
                                    else:
                                        yield InterchangeTrips(camio1, trip1, gasolinera1_1, gasolinera1_2, peticio1_1, peticio1_2, camio2, gasolinera2, peticio2)
                                else:
                                    gasolinera2_1 = trip1[0][0]
                                    peticio2_1 = trip1[0][1]
                                    gasolinera2_2 = trip1[1][0]
                                    peticio2_2 = trip1[1][1]
                                    x1, y1 = self.gasolineras[gasolinera2_1]
                                    x2, y2 = self.centros[camio2]
                                    x3, y3 = self.gasolineras[gasolinera2_2]
                                    distancia1 = abs(x2-x1)+abs(y2-y1)
                                    distancia2 = abs(x3-x1)+abs(y3-y1)
                                    distancia3 = abs(x3-x2)+abs(y3-y2)
                                    km2 = distancia1+distancia2+distancia3
                                    if gasolinera1:
                                        yield InterchangeTrips(camio1, trip1, gasolinera1, peticio1, camio2, gasolinera2_1, gasolinera2_2, peticio2_1, peticio2_2)
                                    else:
                                        yield InterchangeTrips(camio1, trip1, gasolinera1_1, gasolinera1_2, peticio1_1, peticio1_2, camio2, gasolinera2_2, peticio2_1, peticio2_1, peticio2_1)             

    def apply_action(self):
        pass

    def path_cost(self):
        gasolineras, camiones = self.current_state
        camiones = self.current_state[1]
        gasolineras = self.curren
        for 

        distancias = 

    def heuristic(self):
        
        camiones = self.current_state[1]
        costes = [camion[1] for camion in camiones]

        beneficio_total = sum(costes)

        
        

#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params: ProblemParameters):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000)
    
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    gas_stations = [[None for _ in row] for row in peticiones] 
    #  Los índices de las gasolineras coinciden con los de la lista de Gasolineras 
    #  Inicialmente no hay camión que haya satisfecho las peticiones
    #  Una vez esten satisfechas se cambiará None por el índice del camión que la haya satisfecho
    
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
        CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
          
    camions = [[0] for _ in centros]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion
    initial_state =  [gas_stations, camions]


    return initial_state, gasolineras_coords, centros_coords, peticiones



parametres = ProblemParameters(n_distribution_centers= random.randint(1, 10), 
                               n_gas_stations=random.randint(20, 100),
                               multiplicitat=random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0])

initial_state, gasolineras, centros, peticiones = generate_initial_state(parametres)
problem1 = StateRepresentation(initial_state, gasolineras, centros, peticiones)
print(initial_state)

for lista in initial_state:
    print(lista)