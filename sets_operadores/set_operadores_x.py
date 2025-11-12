from typing import Dict, List, Tuple
import random
#  Operadores
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

MAX_VIAJES = 5
MAX_KM = 640
def generate_actionsx(estado):
    camiones = estado.camiones
    # asignar y eliminar
    for idx_camion, camion in enumerate(camiones):
        for idx_posicion in range(len(camion)):
            distancia_anterior1 = estado.km_camiones[idx_camion]
            if len(camion) > 0 and camion[idx_posicion] is not None:
                #  Remove peticion
                copia_camion = camion.copy()
                copia_camion[idx_posicion] = None
                distancia_posterior1 = estado._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                diferencia_dist = distancia_posterior1 - distancia_anterior1
                yield RemovePetition(idx_camion=idx_camion, idx_posicion=idx_posicion, 
                                     diferencia_dist= diferencia_dist)
                #  Move peticion
                for idx_camion2, camion2 in enumerate(camiones):
                    if idx_camion == idx_camion2:
                        continue
                    distancia_anterior2 = estado.km_camiones[idx_camion2]
                    for idx_posicion2 in range(len(camion2) + 1):
                        copia_camion = camion2.copy()
                        copia_camion.insert(idx_posicion2, camion[idx_posicion])
                        
                        if len(copia_camion) < 2 * MAX_VIAJES:
                            distancia_posterior2 = estado._distancia_ruta(camion_id = idx_camion2, ruta = copia_camion)
                            diferencia_dist2 = distancia_posterior2 - distancia_anterior2
                            if distancia_posterior2 < MAX_KM:
                                yield MovePetition(idx_posicion1=idx_posicion, idx_posicion2=idx_posicion2,
                                                idx_camion1=idx_camion, idx_camion2=idx_camion2,
                                                diferencia_dist1= diferencia_dist,
                                                diferencia_dist2= diferencia_dist2)
            #  Intra swap
            for idx_posicion2 in range(len(camion)):
                if idx_posicion != idx_posicion2:
                    copia_camion = camion.copy()
                    copia_camion[idx_posicion] = camion[idx_posicion2]
                    copia_camion[idx_posicion2] = camion[idx_posicion]
                    distancia_posterior1 = estado._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                    diferencia_dist = distancia_posterior1 - distancia_anterior1
                    if distancia_posterior1 < MAX_KM:
                        yield IntraSwap(idx_camion=idx_camion, idx_posicion1=idx_posicion, idx_posicion2=idx_posicion2,
                                        diferencia_dist= diferencia_dist)
    #  Assign Peticion
    for idx_gasolinera in range(len(estado.current_state)):
        for idx_peticion in range(len(estado.current_state[idx_gasolinera])):
            if estado.current_state[idx_gasolinera][idx_peticion] is None:
                for idx_camion, camion in enumerate(camiones):
                    if len(camion) < 2 * MAX_VIAJES:
                        distancia_anterior1 = estado.km_camiones[idx_camion]
                        for idx_posicion in range(len(camion) + 1):
                            copia_camion = camion.copy()
                            copia_camion.insert(idx_posicion, (idx_gasolinera, idx_peticion))
                            distancia_posterior1 = estado._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                            diferencia_dist = distancia_posterior1 - distancia_anterior1
                            if distancia_posterior1 < MAX_KM:
                                yield AssignPetition(idx_gasolinera=idx_gasolinera, idx_peticion=idx_peticion, 
                                                    idx_camion=idx_camion, idx_posicion=idx_posicion,
                                                    diferencia_dist= diferencia_dist)

def generate_one_actionx(estado):
    camiones = estado.camiones
    n_camiones = len(camiones)
    idxs_camion = list(range(n_camiones))
    
    def km(camion_id, ruta=None):
        r = estado.camiones[camion_id] if ruta is None else ruta
        return estado._distancia_ruta(camion_id=camion_id, ruta=r)
    
    def assign():
        libres = [(g, p)
                  for g in range(len(estado.current_state))
                  for p in range(len(estado.current_state[g]))
                  if estado.current_state[g][p] is None]

        if not libres:
            return None
        
        random.shuffle(libres)

        random.shuffle(idxs_camion)
        for g, p in libres:
            for idx_camion in idxs_camion:
                ruta = camiones[idx_camion]
                if len(ruta) < 2 * MAX_VIAJES:
                    pos = random.randrange(len(ruta) + 1)
                    copia_ruta = ruta.copy()
                    copia_ruta.insert(pos, (g,p))
                    distancia_anterior = estado.km_camiones[idx_camion]
                    distancia_posterior = estado._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)

                    if distancia_posterior <= MAX_KM:
                        return AssignPetition(
                            idx_gasolinera= g,
                            idx_peticion=p,
                            idx_camion=idx_camion,
                            idx_posicion=pos,
                            diferencia_dist= distancia_posterior - distancia_anterior
                        )
        return None
    def move():
        candidatos = [(idx_camion, idx_posicion)
                for idx_camion, ruta in enumerate(estado.camiones)
                for idx_posicion in range(len(ruta))
                if ruta and ruta[idx_posicion] is not None]
        random.shuffle(candidatos)
        for idx_camion1, idx_posicion1 in candidatos:
            peticion = estado.camiones[idx_camion1][idx_posicion1]
            ruta1 = estado.camiones[idx_camion1]
            ruta1_post = ruta1.copy()

            ruta1_post[idx_posicion1] = None
            distancia_anterior1 = estado.km_camiones[idx_camion1]
            distancia_posterior1 = estado._distancia_ruta(camion_id=idx_camion1, ruta=ruta1_post)
            diferencia_distancia1 = distancia_posterior1 - distancia_anterior1


            random.shuffle(idxs_camion)
            for idx_camion2 in idxs_camion:
                if idx_camion2 == idx_camion1:
                    continue
                ruta2 = estado.camiones[idx_camion2]
                if len(ruta2) < 2 * MAX_VIAJES:
                    
                    pos2 = random.randrange(len(ruta2) + 1)
                    ruta2_post = ruta2.copy()
                    ruta2_post.insert(pos2, peticion)
                    distancia_anterior2 = estado.km_camiones[idx_camion2]
                    distancia_posterior2 = estado._distancia_ruta(camion_id=idx_camion2, ruta=ruta2_post)
                    if distancia_posterior2 <= MAX_KM:
                        return MovePetition(
                            idx_posicion1=idx_posicion1,
                            idx_posicion2=pos2,
                            idx_camion1=idx_camion1,
                            idx_camion2=idx_camion2,
                            diferencia_dist1=diferencia_distancia1,
                            diferencia_dist2=distancia_posterior2 - distancia_anterior2
                        )
        return None

    def intra_swap():
        random.shuffle(idxs_camion)
        for idx_camion in idxs_camion:
            ruta = estado.camiones[idx_camion]
            pos_validas = [i for i, x in enumerate(ruta) if x is not None]
            if len(pos_validas) < 2:
                continue
            i, j = random.sample(pos_validas, 2)
            copia_ruta = ruta.copy()
            copia_ruta[i], copia_ruta[j] = copia_ruta[j], copia_ruta[i]
            distancia_posterior = estado._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)
            if distancia_posterior <= MAX_KM:
                return IntraSwap(
                    idx_camion=idx_camion,
                    idx_posicion1=i,
                    idx_posicion2=j,
                    diferencia_dist=distancia_posterior - km(idx_camion, ruta)
                )
        return None

    def remove():
        candidatos = [(idx_camion, idx_posicion)
                for idx_camion, ruta in enumerate(camiones)
                for idx_posicion in range(len(ruta))
                if ruta and ruta[idx_posicion] is not None]
        if candidatos:
            idx_camion, idx_posicion = random.choice(candidatos)
            ruta = estado.camiones[idx_camion]
            copia_ruta = ruta.copy()
            # si tu apply_actionx elimina con pop, usa pop aquí también
            copia_ruta[idx_posicion] = None
            distancia_posterior = estado._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)
            return RemovePetition(
                idx_posicion=idx_posicion,
                idx_camion=idx_camion,
                diferencia_dist=distancia_posterior - estado.km_camiones[idx_camion]
            )
        return None
    
    ops = ["assign", "move", "swap", "remove"]
    random.shuffle(ops)

    for op in ops:
        if op == "assign":
            action = assign()
        elif op == "move":
            action = move()
        elif op == "swap":
            action = intra_swap()
        else:
            action = remove()
        if action is not None:
            return [action]
    return None


def apply_actionx(estado, action):
    new_state = estado.copy()
    delta_beneficio, delta_perdida = 0,0
    if isinstance(action, AssignPetition):
        new_state.current_state[action.idx_gasolinera][action.idx_peticion] = True
        new_state.camiones[action.idx_camion].insert(action.idx_posicion, (action.idx_gasolinera, action.idx_peticion))

        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[action.idx_gasolinera][action.idx_peticion]
        delta_beneficio = beneficio_hoy
        delta_perdida = -(beneficio_hoy - beneficio_sig)
        new_state.km_camiones[action.idx_camion] += action.diferencia_dist
        new_state.distancia += action.diferencia_dist

    elif isinstance(action, MovePetition):
        peticion = new_state.camiones[action.idx_camion1][action.idx_posicion1]
        new_state.camiones[action.idx_camion2].insert(action.idx_posicion2, peticion)
        new_state.camiones[action.idx_camion1].pop(action.idx_posicion1)

        new_state.km_camiones[action.idx_camion1] += action.diferencia_dist1
        new_state.km_camiones[action.idx_camion2] += action.diferencia_dist2

        new_state.distancia += action.diferencia_dist1 + action.diferencia_dist2


    elif isinstance(action, RemovePetition):
        gasolinera, peticion = new_state.camiones[action.idx_camion][action.idx_posicion]
        new_state.current_state[gasolinera][peticion] = None
        new_state.camiones[action.idx_camion][action.idx_posicion] = None

        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera][peticion]
        delta_beneficio = -beneficio_hoy
        delta_perdida = beneficio_hoy - beneficio_sig

        new_state.km_camiones[action.idx_camion] += action.diferencia_dist
        new_state.distancia += action.diferencia_dist

    elif isinstance(action, IntraSwap):
        camion = new_state.camiones[action.idx_camion]
        temp = camion[action.idx_posicion1]
        camion[action.idx_posicion1] = camion[action.idx_posicion2]
        camion[action.idx_posicion2] = temp

        new_state.km_camiones[action.idx_camion] += action.diferencia_dist
        new_state.distancia += action.diferencia_dist
        
    new_state.beneficio += delta_beneficio
    new_state.perdida_no_asignadas += delta_perdida
    
    return new_state