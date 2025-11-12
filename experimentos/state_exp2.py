from __future__ import annotations
import random

from typing import Dict, List, Tuple
from Practica_ABIA.abia_Gasolina import *


class StateRepresentation(object):
    
    MAX_KM = 640
    MAX_VIAJES = 5
    MAX_PETICIONES_VIAJE = 2
    dists = None
    dists_gasolineras = None
    beneficio_peticiones = None
    lista_peticiones = None

    def __init__(self, 
                 asignaciones: List[List[int],],
                 camiones:list[list[Tuple,],],
                 km_camiones:list,
                 beneficio:float, 
                 perdida_no_asignadas:float):    
        self.current_state = asignaciones
        self.camiones = camiones
        self.km_camiones = km_camiones
        self.beneficio = beneficio
        self.perdida_no_asignadas = perdida_no_asignadas
        self.perdida = 0

    def _copy_camiones(self):
        camiones_copia = list()
        for camion in self.camiones:
            camion_copia = [camion[0]]
            for viaje in camion[1:]:
                camion_copia.append(list(viaje))
            camiones_copia.append(camion_copia)
        return camiones_copia
    
    def copy(self):

        return StateRepresentation(
            asignaciones= [list(gasolinera) for gasolinera in self.current_state],
            camiones= [camion.copy() for camion in self.camiones],
            km_camiones= self.km_camiones.copy(),
            beneficio= self.beneficio,
            perdida_no_asignadas= self.perdida_no_asignadas
        )

    def __repr__(self) -> str:
        msg = []
        for i, gasolinera in enumerate(self.current_state):
            msg.append(f"Gasolinera {i}:")
            if not gasolinera:
                msg.append(" No tiene peticiones.\n\n")
                continue
            for j in range(len(gasolinera)):
                peticio = self.lista_peticiones[i][j]
                camion = gasolinera[j]
                servicio:str
                if camion is None:
                    servicio = f"No asignada. Dias peticion: {peticio}."
                else:
                    servicio = f"Camion: {camion}. Dias peticion: {peticio}. " 
                
                msg.append(f"\nPeticion {j}: {servicio}")
            
            msg.append("\n\n")
        msg.append(f"\n\nCamiones:\n {self.camiones} \n\nBeneficio total: {self.beneficio}. \nDistancia total: {sum(self.km_camiones)}")
        msg.insert(0, "ASIGNACION FINAL:\n")
        return "".join(msg)
        
    @classmethod
    def preprocessament(cls, gasolineras, centros, peticiones):
        """ Preprocessament de les distàncies i del benefici de les peticions."""
        matriu_distancies = list()
        matriu_distancies_gasolineres = list()
        for gasolinera_coord in gasolineras:
            row = list()
            row2 = list()
            for centro_coord in centros:
                distancia = abs(centro_coord[0] - gasolinera_coord[0]) + abs(centro_coord[1] - gasolinera_coord[1])
                row.append(distancia)
            
            for gasolinera_coord2 in gasolineras:
                distancia = abs(gasolinera_coord2[0] - gasolinera_coord[0]) + abs(gasolinera_coord2[1] - gasolinera_coord[1])
                row2.append(distancia)
            
            matriu_distancies.append(row)
            matriu_distancies_gasolineres.append(row2)
        cls.dists = matriu_distancies
        cls.dists_gasolineras = matriu_distancies_gasolineres

        llista_benefici = list()
        for i in range (len(gasolineras)):
            benefici_gasolinera = list()
            for peticion in peticiones[i]:
                sig_dia = peticion + 1
                porcentaje_hoy = (100 - 2**peticion) / 100 if peticion > 0 else 1.02
                porcentaje_sig = (100 - 2**sig_dia) / 100
                precio = 1000 * porcentaje_hoy
                precio_sig = 1000 * porcentaje_sig
                benefici_gasolinera.append((precio, precio_sig))
            llista_benefici.append(benefici_gasolinera)

        cls.beneficio_peticiones = llista_benefici
        cls.lista_peticiones = peticiones

    @classmethod
    def calcular_distancia(cls, centro, gasolinera1, gasolinera2=None):
        distancia = 0
        distancia += cls.dists[gasolinera1][centro]
        if gasolinera2 is not None:
            distancia += cls.dists_gasolineras[gasolinera1][gasolinera2]
            distancia += cls.dists[gasolinera2][centro]
        else:
            distancia += cls.dists[gasolinera1][centro]
        return distancia
    
    def _dist_c_g(self, camion_id: int, gas_id: int) -> int:
        return self.dists[gas_id][camion_id]

    def _dist_g_g(self, g1: int, g2: int) -> int:
        return self.dists_gasolineras[g1][g2]
    
    def _distancia_ruta(self, camion_id: int, ruta: List[Tuple[int, int]]) -> int:
        distancia = 0
        if ruta and any(ruta):
            for idx_posicion in range(len(ruta)):
                
                peticion = ruta[idx_posicion]
                if peticion is None and ruta[idx_posicion - 1] is None:
                    continue
                elif peticion is None:
                    g = ruta[idx_posicion - 1][0]
                    distancia += self._dist_c_g(camion_id, g)
                elif idx_posicion % 2 != 0 and ruta[idx_posicion - 1] is not None:
                    g_anterior = ruta[idx_posicion - 1][0]
                    g = peticion[0]
                    distancia += self._dist_g_g(g_anterior, g)
                else:
                    g = peticion[0]
                
                distancia += self._dist_c_g(camion_id, g)
        return distancia        

    def heuristic(self):
        return self.beneficio

#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000)
    print("Params:", n_gas, n_centers, multiplicitat, seed, sep="\n")
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    gas_stations = [[None for _ in row] for row in peticiones] 
    #  Los índices de las gasolineras coinciden con los de la lista de Gasolineras 
    #  Inicialmente no hay camión que haya satisfecho las peticiones
    #  Una vez esten satisfechas se cambiará None por el índice del camión que la haya satisfecho
    
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
        CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
    
    camions = [[None] for _ in centros_coords]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion
    km_camiones = [0 for _ in centros_coords]
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    perdida_total = 0
    for gas in range(len(gas_stations)):
        for pet in (range(len(gas_stations[gas]))):
            beneficio_hoy, beneficio_sig = StateRepresentation.beneficio_peticiones[gas][pet]
            perdida_total += beneficio_hoy - beneficio_sig

    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camions,
        km_camiones=km_camiones, 
        beneficio=0,
        perdida_no_asignadas=perdida_total
    )


def generate_initial_state_greedy(params: ProblemParameters, seed = None):
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000) if seed== None else seed
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    gas_stations = [[None for _ in row] for row in peticiones] 
    #  Los índices de las gasolineras coinciden con los de la lista de Gasolineras 
    #  Inicialmente no hay camión que haya satisfecho las peticiones
    #  Una vez esten satisfechas se cambiará None por el índice del camión que la haya satisfecho
    
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
    CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    clusters = []

    for gas in range(len(gasolineras_coords)):
        distancias = []
        for centro in range(len(centros_coords)):
            dist = StateRepresentation.dists[gas][centro]
            distancias.append(dist)
        cluster_asignado = distancias.index(min(distancias))
        clusters.append(cluster_asignado)
    
    camiones = [[] for _ in centros_coords]
    km_camiones = [0 for _ in centros_coords]
    distancia_total = 0
    beneficio_total = 0
    for id_camion in range(len(centros_coords)):

        peticiones_cluster = []

        for id_gasolinera, id_cluster in enumerate(clusters):
            if id_cluster == id_camion:
                for id_peticion, dias in enumerate(peticiones[id_gasolinera]):
                    porcentaje = max(0, 100 - 2**dias) / 100 if dias > 0 else 1.02
                    beneficio = 1000 * porcentaje
                    peticiones_cluster.append((beneficio, id_gasolinera, id_peticion))
        
        #  ordenamos por beneficio:
        peticiones_cluster.sort(reverse=True, key = lambda x: x[0])

        km = 0
        num_viajes = 0
        peticiones_asignadas = set()

        while peticiones_cluster and num_viajes < 5:
            peticion_actual = None

            for pet in peticiones_cluster:
                if (pet[1], pet[2]) not in peticiones_asignadas:
                    peticion_actual = pet
                    break
            
            if peticion_actual is None: break

            beneficio1, gas1, pet1 = peticion_actual
            
            beneficio2, gas2, pet2 = 0, None, None
            min_dist = float('inf')

            for pet in peticiones_cluster:
                if (pet[1], pet[2]) not in peticiones_asignadas and pet[1] != gas1:
                    dist = StateRepresentation.dists_gasolineras[gas1][pet[1]]

                    if dist < min_dist:
                        min_dist = dist
                        beneficio2, gas2, pet2 = pet
        
            if gas2 is not None:
                viaje = [(gas1, pet1), (gas2, pet2)]
            else:
                viaje = [(gas1, pet1)]
            km_viaje = StateRepresentation.calcular_distancia(centro = id_camion, 
                                                                gasolinera1= viaje[0][0], 
                                                                gasolinera2= None if len(viaje) < 2 else viaje[1][0])
            
            if km + km_viaje <= 640:
                camiones[id_camion].extend(viaje)
                km_camiones[id_camion] += km_viaje
                km += km_viaje
                distancia_total += km_viaje
                beneficio_total += beneficio1
                num_viajes += 1
                peticiones_asignadas.add((gas1, pet1))
                gas_stations[gas1][pet1] = id_camion

                if gas2 is not None:
                    peticiones_asignadas.add((gas2, pet2))
                    gas_stations[gas2][pet2] = id_camion
                    beneficio_total += beneficio2
            else:
                break
    perdida_total = 0
    for gas in range(len(gas_stations)):
        for pet in (range(len(gas_stations[gas]))):
            if gas_stations[gas][pet] == None:
                beneficio_hoy, beneficio_sig = StateRepresentation.beneficio_peticiones[gas][pet]
                perdida_total += beneficio_hoy - beneficio_sig
    print(beneficio_total, perdida_total, distancia_total)
    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camiones,
        km_camiones=km_camiones,
        beneficio=beneficio_total,
        perdida_no_asignadas= perdida_total
    )

