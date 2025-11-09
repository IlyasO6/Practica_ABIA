#  Operadores 3
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


def generate_actions_3(estado):
    camiones = estado.camiones
    # Remove, Move, Swap 
    for idx_camion_1, camion_1 in enumerate(camiones):
        #  si el camion no tiene viajes, skip:
        if len(camion_1) < 2:
            continue
        for idx_viaje_camion_1 in range(1, len(camion_1)):
            viaje_1 = camion_1[idx_viaje_camion_1] #  no hace falta comprobar que exista, ya que no pueden haber listas vacias
            dist_viaje_1_anterior = estado._distancia_viaje(idx_camion_1, viaje_1)
            
            for idx_peticion_camion_1 in range(len(viaje_1)):
                id_gas_camion_1, id_peticion_camion_1 = viaje_1[idx_peticion_camion_1]
                #  eliminamos la peticion actual del viaje, y evaluamos la nueva distancia:
                viaje_camion_1_post = viaje_1[:idx_peticion_camion_1] + viaje_1[idx_peticion_camion_1 + 1:]
                dist_viaje_1_post = estado._distancia_viaje(idx_camion_1, viaje_camion_1_post)
                #  diferencia (delta) de distancia de viaje tras eliminar la petición:
                dist_reducida = dist_viaje_1_post - dist_viaje_1_anterior
                yield RemovePeticion(
                    id_camion=idx_camion_1, id_viaje=idx_viaje_camion_1, id_peticion=idx_peticion_camion_1,
                    distancia_reducida=dist_reducida
                    )
                for idx_camion_2, camion_2 in enumerate(camiones):
                    for idx2 in range(1, len(camion_2)):
                        viaje_2 = camion_2[idx2]
                        dist_viaje_2_anterior = estado._distancia_viaje(idx_camion_2, viaje_2)
                        #  comprobamos restricciones:
                        if (idx_camion_1 != idx_camion_2 or idx_viaje_camion_1 != idx2) and len(viaje_2) < estado.MAX_PETICIONES_VIAJE:
                            #  calculamos distancias:
                            delta_origen = dist_reducida
                            dist_viaje_2_post = estado._distancia_viaje(idx_camion_2, viaje_2 + [(id_gas_camion_1, id_peticion_camion_1)])
                            delta_desti = dist_viaje_2_post - dist_viaje_2_anterior 
                            #  comprobamos que se cumplan las restricciones 
                            if camiones[idx_camion_2][0] + delta_desti <= estado.MAX_KM:
                                yield MovePeticion(
                                    camion_origen=idx_camion_1, viaje_origen=idx_viaje_camion_1, pos_origen=idx_peticion_camion_1,
                                    camion_destino=idx_camion_2, viaje_destino=idx2,
                                    distancia_reducida=delta_origen, distancia_adicional=delta_desti
                                )
                        for idx_peticion_camion_2 in range(len(viaje_2)):
                            if idx_camion_1 == idx_camion_2 and idx_viaje_camion_1 == idx2 and idx_peticion_camion_1 == idx_peticion_camion_2:
                                continue
                            if (idx_camion_1, idx_viaje_camion_1, idx_peticion_camion_1) >= (idx_camion_2, idx2, idx_peticion_camion_2):
                                continue
                            #  copiamos las listas de los viajes en listas temporales:
                            nuevo_v1 = [tupla for tupla in viaje_1]
                            nuevo_v2 = [tupla for tupla in viaje_2] 
                            #  intercambiamos las respectivas peticiones:
                            nuevo_v1[idx_peticion_camion_1] = viaje_2[idx_peticion_camion_2]
                            nuevo_v2[idx_peticion_camion_2] = viaje_1[idx_peticion_camion_1]
                            #  recalculamos distancias:
                            dist_nuevo_v1 = estado._distancia_viaje(idx_camion_1, nuevo_v1)
                            dist_nuevo_v2 = estado._distancia_viaje(idx_camion_2, nuevo_v2)
                            delta_viaje_camion_1 = dist_nuevo_v1 - dist_viaje_1_anterior
                            delta_viaje_camion_2 = dist_nuevo_v2 - dist_viaje_2_anterior
                            #  comprobamos que se cumplan las restricciones 
                            if camiones[idx_camion_1][0] + delta_viaje_camion_1 <= estado.MAX_KM and camiones[idx_camion_2][0] + delta_viaje_camion_2 <= estado.MAX_KM:
                                yield SwapPeticiones(
                                    id_camion_1=idx_camion_1, id_viaje_1=idx_viaje_camion_1, pos_1=idx_peticion_camion_1,
                                    id_camion_2=idx_camion_2, id_viaje_2=idx2, pos_2=idx_peticion_camion_2,
                                    delta_camion1=delta_viaje_camion_1, delta_camion2=delta_viaje_camion_2
                                )
    #  InsertViaje y FillViaje
    for idx_gasolinera in range(len(estado.current_state)):
        for idx_peticio in range(len(estado.current_state[idx_gasolinera])):
            if estado.current_state[idx_gasolinera][idx_peticio] is None: #  la peticion no está asignada
                for idx_camion, camion in enumerate(estado.camiones):
                    if len(camion) - 1 < estado.MAX_VIAJES:
                        distancia_adicional = 2 * estado._dist_c_g(idx_camion, idx_gasolinera)
                        if camion[0] + distancia_adicional <= estado.MAX_KM:
                            yield InsertViaje(
                                id_camion=idx_camion, id_gasolinera=idx_gasolinera, id_peticion=idx_peticio,
                                distancia_adicional=distancia_adicional
                            )
                    # FillViaje: añadir segunda petición a un viaje existente de 1 petición
                    for idx_viaje in range(1, len(camion)):
                        viaje = camion[idx_viaje]
                        if viaje and len(viaje) < estado.MAX_PETICIONES_VIAJE:
                            distancia_ant = estado._distancia_viaje(idx_camion, viaje)
                            distancia_post = estado._distancia_viaje(idx_camion, viaje + [(idx_gasolinera, idx_peticio)])
                            add = distancia_post - distancia_ant
                            if camion[0] + add <= estado.MAX_KM:
                                yield FillViaje(
                                    id_camion=idx_camion, id_viaje=idx_viaje, id_gasolinera=idx_gasolinera,
                                    id_peticion=idx_peticio, distancia_adicional=add
                                )
                        
def apply_action_3(estado, action: Operators):
    new_state = estado.copy()
    delta_beneficio, delta_perdida = 0,0
    if isinstance(action, RemovePeticion):
        #  parametros del operador:
        camion = action.id_camion
        viaje = action.id_viaje
        peticion = action.id_peticion
        distancia_reducida = action.distancia_reducida
        # Actualizamos asignación
        gasolinera, peticion_idx = new_state.camiones[camion][viaje][peticion]
        #  Actualizamos beneficio y perdida:
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera][peticion_idx]
        delta_perdida = beneficio_hoy - beneficio_sig
        delta_beneficio = -beneficio_hoy
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
        new_state.camiones[camion][0] += distancia_reducida
        new_state.distancia += distancia_reducida
    
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
        #  Actualizamos beneficio y perdida:
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[id_gasolinera][id_peticion]
        delta_beneficio = beneficio_hoy
        delta_perdida = -(beneficio_hoy - beneficio_sig)
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
        #  Actualizamos beneficio y perdida:
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[id_gasolinera][id_peticion]
        delta_beneficio = beneficio_hoy
        delta_perdida = -(beneficio_hoy - beneficio_sig)
        #  Actualizamos asignación
        new_state.current_state[id_gasolinera][id_peticion] = id_camion
        #  Añadimos la petición al viaje del camión y actualizamos distancias:
        new_state.camiones[id_camion][id_viaje].append((id_gasolinera, id_peticion))
        new_state.camiones[id_camion][0] += distancia_adicional
        new_state.distancia += distancia_adicional
    
    new_state.beneficio += delta_beneficio
    new_state.perdida_no_asignadas += delta_perdida
    return new_state
