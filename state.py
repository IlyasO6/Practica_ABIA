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
            camiones= self._copy_camiones(),
            beneficio= self.beneficio,
            distancia= self.distancia,
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
        camiones = self._copy_camiones()
        # Remove, Move, Swap 
        for idx_camion_1, camion_1 in enumerate(camiones):
            #  si el camion no tiene viajes, skip:
            if len(camion_1) < 2:
                continue
            for idx_viaje_camion_1 in range(1, len(camion_1)):
                viaje_1 = camion_1[idx_viaje_camion_1] #  no hace falta comprobar que exista, ya que no pueden haber listas vacias
                dist_viaje_1_anterior = self._distancia_viaje(idx_camion_1, viaje_1)
                
                for idx_peticion_camion_1 in range(len(viaje_1)):
                    id_gas_camion_1, id_peticion_camion_1 = viaje_1[idx_peticion_camion_1]
                    #  eliminamos la peticion actual del viaje, y evaluamos la nueva distancia:
                    viaje_camion_1_post = viaje_1[:idx_peticion_camion_1] + viaje_1[idx_peticion_camion_1 + 1:]
                    dist_viaje_1_post = self._distancia_viaje(idx_camion_1, viaje_camion_1_post)
                    #  diferencia (delta) de distancia de viaje tras eliminar la petición:
                    dist_reducida = dist_viaje_1_post - dist_viaje_1_anterior
                    yield RemovePeticion(
                        id_camion=idx_camion_1, id_viaje=idx_viaje_camion_1, id_peticion=idx_peticion_camion_1,
                        distancia_reducida=dist_reducida
                        )
                    for idx_camion_2, camion_2 in enumerate(camiones):
                        for idx2 in range(1, len(camion_2)):
                            viaje_2 = camion_2[idx2]
                            dist_viaje_2_anterior = self._distancia_viaje(idx_camion_2, viaje_2)
                            #  comprobamos restricciones:
                            if (idx_camion_1 != idx_camion_2 or idx_viaje_camion_1 != idx2) and len(viaje_2) < self.MAX_PETICIONES_VIAJE:
                                #  calculamos distancias:
                                delta_origen = dist_reducida
                                dist_viaje_2_post = self._distancia_viaje(idx_camion_2, viaje_2 + [(id_gas_camion_1, id_peticion_camion_1)])
                                delta_desti = dist_viaje_2_post - dist_viaje_2_anterior 
                                #  comprobamos que se cumplan las restricciones 
                                if camiones[idx_camion_2][0] + delta_desti <= self.MAX_KM:
                                    yield MovePeticion(
                                        camion_origen=idx_camion_1, viaje_origen=idx_viaje_camion_1, pos_origen=idx_peticion_camion_1,
                                        camion_destino=idx_camion_2, viaje_destino=idx2,
                                        distancia_reducida=delta_origen, distancia_adicional=delta_desti
                                    )
                            for idx_peticion_camion_2 in range(len(viaje_2)):
                                if idx_camion_1 == idx_camion_2 and idx_viaje_camion_1 == idx2 and idx_peticion_camion_1 == idx_peticion_camion_2:
                                    continue
                                #  copiamos las listas de los viajes en listas temporales:
                                nuevo_v1 = [tupla for tupla in viaje_1]
                                nuevo_v2 = [tupla for tupla in viaje_2] 
                                #  intercambiamos las respectivas peticiones:
                                nuevo_v1[idx_peticion_camion_1] = viaje_2[idx_peticion_camion_2]
                                nuevo_v2[idx_peticion_camion_2] = viaje_1[idx_peticion_camion_1]
                                #  recalculamos distancias:
                                dist_nuevo_v1 = self._distancia_viaje(idx_camion_1, nuevo_v1)
                                dist_nuevo_v2 = self._distancia_viaje(idx_camion_2, nuevo_v2)
                                delta_viaje_camion_1 = dist_nuevo_v1 - dist_viaje_1_anterior
                                delta_viaje_camion_2 = dist_nuevo_v2 - dist_viaje_2_anterior
                                #  comprobamos que se cumplan las restricciones 
                                if camiones[idx_camion_1][0] + delta_viaje_camion_1 <= self.MAX_KM and camiones[idx_camion_2][0] + delta_viaje_camion_2 <= self.MAX_KM:
                                    yield SwapPeticiones(
                                        id_camion_1=idx_camion_1, id_viaje_1=idx_viaje_camion_1, pos_1=idx_peticion_camion_1,
                                        id_camion_2=idx_camion_2, id_viaje_2=idx2, pos_2=idx_peticion_camion_2,
                                        delta_camion1=delta_viaje_camion_1, delta_camion2=delta_viaje_camion_2
                                    )
        #  InsertViaje y FillViaje
        for idx_gasolinera in range(len(self.current_state)):
            for idx_peticio in range(len(self.current_state[idx_gasolinera])):
                if self.current_state[idx_gasolinera][idx_peticio] is None: #  la peticion no está asignada
                    for idx_camion, camion in enumerate(self.camiones):
                        if len(camion) - 1 < self.MAX_VIAJES:
                            distancia_adicional = 2 * self._dist_c_g(idx_camion, idx_gasolinera)
                            if camion[0] + distancia_adicional <= self.MAX_KM:
                                yield InsertViaje(
                                    id_camion=idx_camion, id_gasolinera=idx_gasolinera, id_peticion=idx_peticio,
                                    distancia_adicional=distancia_adicional
                                )
                        # FillViaje: añadir segunda petición a un viaje existente de 1 petición
                        for idx_viaje in range(1, len(camion)):
                            viaje = camion[idx_viaje]
                            if viaje and len(viaje) < self.MAX_PETICIONES_VIAJE:
                                distancia_ant = self._distancia_viaje(idx_camion, viaje)
                                distancia_post = self._distancia_viaje(idx_camion, viaje + [(idx_gasolinera, idx_peticio)])
                                add = distancia_post - distancia_ant
                                if camion[0] + add <= self.MAX_KM:
                                    yield FillViaje(
                                        id_camion=idx_camion, id_viaje=idx_viaje, id_gasolinera=idx_gasolinera,
                                        id_peticion=idx_peticio, distancia_adicional=add
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
            gasolinera, peticion = new_state.camiones[camion_origen][viaje_origen][pos_origen]
            new_state.current_state[gasolinera][peticion] = camion_destino
            #  Movemos la petición del viaje origen al viaje destino:
            del new_state.camiones[camion_origen][viaje_origen][pos_origen]
            new_state.camiones[camion_destino][viaje_destino].append((gasolinera, peticion))
            #  actualizamos distancias
            new_state.camiones[camion_origen][0] -= distancia_reducida
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

