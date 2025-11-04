from __future__ import annotations
import random

from typing import Dict, List, Tuple
from operators import *
from abia_Gasolina import *
from problem_parameters import ProblemParameters


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
                 camiones:list[list[int, Tuple,],],
                 beneficio:float, 
                 distancia:float):    
        self.current_state = asignaciones
        self.camiones = camiones
        self.beneficio = beneficio
        self.distancia = distancia
        self.perdida = 0
        self.dists:list
        self.dists_gasolineras:list


    def copy(self):

        asignaciones_copia = [list(gasolinera) for gasolinera in self.current_state]
        camiones_copia = []
        for camion in self.camiones:
            camion_copia = [camion[0]]
            for viaje in camion[1:]:
                camion_copia.append(list(viaje))
            camiones_copia.append(camion_copia)

        return StateRepresentation(
            asignaciones=asignaciones_copia,
            camiones=camiones_copia,
            beneficio=self.beneficio,
            distancia=self.distancia,
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
        msg.append(f"\n\nCamiones:\n {self.camiones} \n\nBeneficio total: {self.beneficio - self.perdida}")
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
                porcentaje_sig = (100 - 2**sig_dia)
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

    def _distancia_viaje(self, camion_id: int, viaje: List[Tuple[int, int]]) -> int:
        if not viaje:
            return 0
        g1 = viaje[0][0]
        if len(viaje) == 1:
            return 2 * self._dist_c_g(camion_id, g1)
        g2 = viaje[1][0]
        return self._dist_c_g(camion_id, g1) + self._dist_g_g(g1, g2) + self._dist_c_g(camion_id, g2)
    
    def generate_actions(self):
        # Remove, Move, Swap 
        camiones = [camion for camion in self.camiones]
        for i, camion1 in enumerate(camiones):
            if len(camion1) <= 1:
                continue
            for idx in range(1, len(camion1)):
                viaje_1 = camion1[idx]
                if not viaje_1:
                    continue
                old_v1 = self._distancia_viaje(i, viaje_1)
                for pos_1 in range(len(viaje_1)):
                    gas_actual, pet_idx = viaje_1[pos_1]
                    
                    # RemovePeticion
                    v1_after = viaje_1[:pos_1] + viaje_1[pos_1 + 1:]
                    new_v1 = self._distancia_viaje(i, v1_after)
                    delta_remove = old_v1 - new_v1
                    yield RemovePeticion(
                        id_camion=i, id_viaje=idx, id_peticion=pos_1,
                        distancia_reducida=delta_remove
                        )
                    
                    for j, camion2 in enumerate(camiones):
                        for idx2 in range(1, len(camion2)):
                            viaje_2 = camion2[idx2]

                            # MovePeticion
                            if (i != j or idx != idx2) and viaje_2 and len(viaje_2) < self.MAX_PETICIONES_VIAJE:
                                old_o = old_v1
                                new_o = new_v1 
                                delta_o = old_o - new_o 

                                old_d = self._distancia_viaje(j, viaje_2)
                                new_d = self._distancia_viaje(j, viaje_2 + [(gas_actual, pet_idx)])
                                delta_d = new_d - old_d 

                                if camiones[i][0] - delta_o <= self.MAX_KM and camiones[j][0] + delta_d <= self.MAX_KM:
                                    yield MovePeticion(
                                        camion_origen=i, viaje_origen=idx, pos_origen=pos_1,
                                        camion_destino=j, viaje_destino=idx2,
                                        distancia_reducida=delta_o, distancia_adicional=delta_d
                                    )

                            # SwapPeticiones
                            if not viaje_2:
                                continue

                            old_v2 = self._distancia_viaje(j, viaje_2)
                            for pos_2 in range(len(viaje_2)):
                                if i == j and idx == idx2 and pos_1 == pos_2:
                                    continue
                                nuevo_v1 = [tupla for tupla in viaje_1]
                                nuevo_v2 = [tupla for tupla in viaje_2] 
                                nuevo_v1[pos_1] = viaje_2[pos_2]
                                nuevo_v2[pos_2] = viaje_1[pos_1]
                                new1 = self._distancia_viaje(i, nuevo_v1)
                                new2 = self._distancia_viaje(j, nuevo_v2)
                                delta1 = new1 - old_v1
                                delta2 = new2 - old_v2

                                if camiones[i][0] + delta1 <= self.MAX_KM and camiones[j][0] + delta2 <= self.MAX_KM:
                                    yield SwapPeticiones(
                                        id_camion_1=i, id_viaje_1=idx, pos_1=pos_1,
                                        id_camion_2=j, id_viaje_2=idx2, pos_2=pos_2,
                                        delta_camion1=delta1, delta_camion2=delta2
                                    )

        # InsertViaje y FillViaje
        for gasolinera in range(len(self.current_state)):
            for peticio in range(len(self.current_state[gasolinera])):
                if self.current_state[gasolinera][peticio] is None:
                    for i, camion in enumerate(self.camiones):
                        # InsertViaje: crear viaje nuevo con una única petición
                        if len(camion) - 1 < self.MAX_VIAJES:
                            distancia_add = 2 * self._dist_c_g(i, gasolinera)
                            if camion[0] + distancia_add <= self.MAX_KM:
                                yield InsertViaje(
                                    id_camion=i, id_gasolinera=gasolinera, id_peticion=peticio,
                                    distancia_adicional=distancia_add
                                )
                        # FillViaje: añadir como segunda petición a un viaje existente de 1 petición
                        for idx in range(1, len(camion)):
                            viaje = camion[idx]
                            if viaje and len(viaje) < self.MAX_PETICIONES_VIAJE:
                                old_v = self._distancia_viaje(i, viaje)
                                new_v = self._distancia_viaje(i, viaje + [(gasolinera, peticio)])
                                add = new_v - old_v
                                if camion[0] + add <= self.MAX_KM:
                                    yield FillViaje(
                                        id_camion=i, id_viaje=idx, id_gasolinera=gasolinera,
                                        id_peticion=peticio, distancia_adicional=add
                                    )
                            
    def apply_action(self, action: Operators) -> StateRepresentation:
        new_state = self.copy()
        if isinstance(action, RemovePeticion):
            #  parametros del operador:
            camion = action.id_camion
            viaje = action.id_viaje
            peticion = action.id_peticion
            distancia_reducida = action.distancia_reducida
            # Actualizamos asignación
            gasolinera, peticion_idx = new_state.camiones[camion][viaje][peticion]
            #  Si eliminamos la primera peticion y hay una segunda, movemos la segunda a la primera posición: 
            if peticion_idx == 0 and len(new_state.current_state[gasolinera]) > 1 and new_state.current_state[gasolinera][1] is not None:
                new_state.current_state[gasolinera][peticion_idx] = new_state.current_state[gasolinera][1]
                new_state.current_state[gasolinera][1] = None
            else:
                new_state.current_state[gasolinera][peticion_idx] = None
            #  Eliminamos la petición del viaje del camion:
            del new_state.camiones[camion][viaje][peticion]
            if not new_state.camiones[camion][viaje]:
                del new_state.camiones[camion][viaje]
            #  actualizamos distancias:
            new_state.camiones[camion][0] -= distancia_reducida
            new_state.distancia -= distancia_reducida
        
        elif isinstance(action, MovePeticion):
            
            #  parametros del operador:
            camion_origen = action.camion_origen
            viaje_origen = action.viaje_origen
            pos_origen = action.pos_origen
            camion_destino = action.camion_destino
            viaje_destino = action.viaje_destino
            distancia_reducida = action.distancia_reducida
            distancia_adicional = action.distancia_adicional
            
            #  Actualizamos asignación
            #print("\nNUEVA ITER")
            #print(new_state.camiones, camion_origen, viaje_origen, pos_origen, sep="\n")
            gasolinera, peticion = new_state.camiones[camion_origen][viaje_origen][pos_origen]
            new_state.current_state[gasolinera][peticion] = camion_destino
            #  Movemos la petición del viaje origen al viaje destino y modificamos distancias:
            del new_state.camiones[camion_origen][viaje_origen][pos_origen]

            new_state.camiones[camion_origen][0] -= distancia_reducida
            new_state.camiones[camion_destino][viaje_destino].append((gasolinera, peticion))
            new_state.camiones[camion_destino][0] += distancia_adicional
            new_state.distancia += distancia_adicional - distancia_reducida
            
            if not new_state.camiones[camion_origen][viaje_origen]:
                del new_state.camiones[camion_origen][viaje_origen]
        
        elif isinstance(action, SwapPeticiones):
            #  parametros del operador:
            id_camion_1 = action.id_camion_1
            id_viaje_1 = action.id_viaje_1
            pos_1 = action.pos_1
            id_camion_2 = action.id_camion_2
            id_viaje_2 = action.id_viaje_2
            pos_2 = action.pos_2
            delta1 = action.delta_camion1
            delta2 = action.delta_camion2
            #  Actualizamos asignación
            gasolinera1, peticion1 = new_state.camiones[id_camion_1][id_viaje_1][pos_1]
            gasolinera2, peticion2 = new_state.camiones[id_camion_2][id_viaje_2][pos_2]
            new_state.current_state[gasolinera1][peticion1] = id_camion_2
            new_state.current_state[gasolinera2][peticion2] = id_camion_1
            #  Intercambiamos las peticiones en los viajes correspondientes y actualizamos distancias:
            new_state.camiones[id_camion_1][id_viaje_1][pos_1] = (gasolinera2, peticion2)
            new_state.camiones[id_camion_2][id_viaje_2][pos_2] = (gasolinera1, peticion1)
            new_state.camiones[id_camion_1][0] += delta1
            new_state.camiones[id_camion_2][0] += delta2
            new_state.distancia += (delta1 + delta2)
        
        elif isinstance(action, InsertViaje):
            #  parametros del operador:
            id_camion = action.id_camion
            id_gasolinera = action.id_gasolinera
            id_peticion = action.id_peticion
            distancia_adicional = action.distancia_adicional
            #  Actualizamos asignación
            new_state.current_state[id_gasolinera][id_peticion] = id_camion
            #  Añadimos el nuevo viaje al camión y actualizamos distancias:
            new_state.camiones[id_camion].append([(id_gasolinera, id_peticion)])
            new_state.camiones[id_camion][0] += distancia_adicional
            new_state.distancia += distancia_adicional
        
        elif isinstance(action, FillViaje):
            #  parametros del operador:
            id_camion = action.id_camion
            id_viaje = action.id_viaje
            id_gasolinera = action.id_gasolinera
            id_peticion = action.id_peticion
            distancia_adicional = action.distancia_adicional
            #  Actualizamos asignación
            new_state.current_state[id_gasolinera][id_peticion] = id_camion
            #  Añadimos la petición al viaje del camión y actualizamos distancias:
            new_state.camiones[id_camion][id_viaje].append((id_gasolinera, id_peticion))
            new_state.camiones[id_camion][0] += distancia_adicional
            new_state.distancia += distancia_adicional

        return new_state

    def path_cost(self):
        perdida = self.distancia * 2  # Coste por km recorrido
        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                #  sumamos las perdidas por peticiones no satisfechas:
                if self.current_state[i][j] == None:
                    beneficio_hoy, beneficio_sig = self.beneficio_peticiones[i][j]
                    perdida += beneficio_hoy - beneficio_sig
        self.perdida = perdida
        return -perdida
            

    def heuristic(self):
        beneficio_total = 0
        for i in range(len(self.current_state)):
            for j in range(len(self.current_state[i])):
                #  sumamos solo las peticiones satisfechas:
                if self.current_state[i][j] != None:
                    beneficio, _ = self.beneficio_peticiones[i][j]
                    beneficio_total += beneficio
        self.beneficio = beneficio_total
        return -beneficio_total

#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state(params: ProblemParameters):
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
    
    camions = [[0] for _ in centros_coords]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion

    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)
    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camions,
        beneficio=0,
        distancia=0
    )


def generate_initial_state_greedy(params: ProblemParameters):
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
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    clusters = []

    for gas in range(len(gasolineras_coords)):
        distancias = []
        for centro in range(len(centros_coords)):
            dist = StateRepresentation.dists[gas][centro]
            distancias.append(dist)
        cluster_asignado = distancias.index(min(distancias))
        clusters.append(cluster_asignado)
    
    camiones = [[0] for _ in centros_coords]

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
                camiones[id_camion].append(viaje)
                camiones[id_camion][0] += km_viaje
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
    print(beneficio_total)
    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camiones,
        beneficio=beneficio_total,
        distancia=distancia_total
    )

