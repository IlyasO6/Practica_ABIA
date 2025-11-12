from typing import Dict, List, Tuple
import random

#_______________________________________________________________________________________________________________
#  Operadores
class GasOperators(object):
    def __init__(self):
        pass

class AddOnlyTrip(GasOperators):
    def __init__(self, km, idx_gasolinera, idx_peticio, idx_camio):  # tenemos los índices para aplicar la operación en nuestra representación del estado
        self.idx_gasolinera = idx_gasolinera                        
        self.idx_peticio = idx_peticio
        self.idx_camio = idx_camio
        self.km = km        #  tenemos los km cambiados para sumarlos a la distancia recorrida del camión

    def __repr__(self) -> str:
        return (
            f"Camió {self.idx_camio} assoleix petició {self.idx_peticio} "
            f"de la benzinera {self.idx_gasolinera} i torna al centre de distribució."
        )

class AddMultipleTrip(GasOperators):
    def __init__(self, km, idx_gasolinera1, idx_gasolinera2, idx_peticio1, idx_peticio2, idx_camio):
        self.idx_gasolinera1 = idx_gasolinera1
        self.idx_peticio1 = idx_peticio1
        self.idx_gasolinera2 = idx_gasolinera2
        self.idx_peticio2 = idx_peticio2
        self.idx_camio = idx_camio
        self.km = km

    def __repr__(self) -> str:
        return (
            f"Camió {self.idx_camio} assoleix la petició {self.idx_peticio1} "
            f"de la benzinera {self.idx_gasolinera1} després assoleix la petició "
            f"{self.idx_peticio2} de la benzinera {self.idx_gasolinera2} i torna al centre de distribució."
        )


class RemoveTrip(GasOperators):
    def __init__(
        self,
        km:float,
        idx_camio:int,
        idx_stop1:int,
        idx_gasolinera1:int,
        idx_peticio1:int,
        idx_gasolinera2=None,
        idx_peticio2=None,
    ): 
        self.idx_camio = idx_camio
        self.idx_stop1 = idx_stop1
        self.km = km
        self.idx_gasolinera2 = idx_gasolinera2
        self.idx_peticio2 = idx_peticio2
        self.idx_gasolinera1 = idx_gasolinera1
        self.idx_peticio1 = idx_peticio1

    def __repr__(self) -> str:
        if self.idx_gasolinera2 is None and self.idx_peticio2 is None:
            return (
                f"Eliminem l'assoliment de la petició {self.idx_peticio1} "
                f"de la benzinera {self.idx_gasolinera1}"
            )
        else:
            return (
                f"Eliminem l'assoliment de les peticions: {self.idx_peticio1} "
                f"de la benzinera {self.idx_gasolinera1} i {self.idx_peticio2} "
                f"de la benzinera {self.idx_gasolinera2}"
            )
#_______________________________________________________________________________________________________________
#  Generate Action
def generate_actions1x(estado):
    MAX_VIAJES = 5
    MAX_KM = 640
    camiones = estado._copy_camiones()
    gasolineras = [list(gasolinera) for gasolinera in estado.current_state]
    for idx_gasolinera, gasolinera in enumerate(gasolineras):
        for idx_peticio in range(len(gasolinera)):
            if gasolinera[idx_peticio] is None:
                for idx_gasolinera2, gasolinera2 in enumerate(gasolineras):
                    for idx_peticio2 in range(len(gasolinera2)):
                        if gasolinera2[idx_peticio2] is None and (idx_gasolinera != idx_gasolinera2 or idx_peticio != idx_peticio2):
                            for idx_camio, camio in enumerate(camiones):
                                distancia = estado._dist_c_g(idx_camio, idx_gasolinera)
                                km = distancia*2
                                km2 = distancia + estado._dist_c_g(idx_gasolinera, idx_gasolinera2) + estado._dist_c_g(idx_camio, idx_gasolinera2)                            
                                if estado.km_camiones[idx_camio]+km2 < MAX_KM and len(camio) < 2 * MAX_VIAJES:
# AddOnlyTrip                                
                                    yield AddOnlyTrip(km, idx_gasolinera, idx_peticio, idx_camio)
# AddMultipleTrip 
                                    yield AddMultipleTrip(km2, idx_gasolinera, idx_gasolinera2, idx_peticio, idx_peticio2, idx_camio)                          
                                elif estado.km_camiones[idx_camio]+km < MAX_KM and len(camio) < 2 * MAX_VIAJES:
                                    yield AddOnlyTrip(km, idx_gasolinera, idx_peticio, idx_camio)                           
# RemoveTrip
                                if len(camio) > 0: # mirem si el camio té algun viatge
                                    for idx_tupla in range(0, len(camio), 2): # Vamos de 2 en 2 pues cada viaje esta formado por 2 tuplas y con estos operadores la primera siempre será not None
                                        tupla = camio[idx_tupla]
                                        tupla2 = camio[idx_tupla+1] if camio[idx_tupla+1] is not None else None
                                        idx_g = tupla[0] #  Posem idx_g per referir-nos a l'índex de la benzinera per no reescriure idx_gasolinera, no volem possibles bugs (no crec que passi res però per si de cas)
                                        idx_p = tupla[1] #  Igual que amb la benzinera
                                        distancia = estado._dist_c_g(idx_camio, idx_g)
                                        km = distancia*2
                                        if tupla2 is not None:
                                            idx_g2 = tupla2[0]
                                            idx_p2 = tupla2[1]
                                            km2 = distancia + estado._dist_c_g(idx_g, idx_g2) + estado._dist_c_g(idx_camio, idx_g2)
                                        else:
                                            idx_g2 = None
                                            idx_p2 = None
                                            yield RemoveTrip(km, idx_camio, idx_tupla, idx_g, idx_p, idx_g2, idx_p2)

#_______________________________________________________________________________________________________________
#  Generate One Action
def generate_one_action1x(estado):
    random_value = random.random()
    operador = 0
    if random_value < (1/3):
        operador = 1
    elif random_value < (2/3):
        operador = 2
    
    MAX_VIAJES = 5
    MAX_KM = 640

    gasolineras = [list(gasolinera) for gasolinera in estado.current_state]
    for idx_gasolinera, gasolinera in enumerate(gasolineras):
        validas = [idx_gasolinera for i in gasolinera if i is None] #  Afegim les gasolineres per cada petició buida que tenen
        random_value = random.random()
        idx_gasolinera1 = validas.pop(random_value*len(validas))
        random_value = random.random()
        idx_gasolinera2 = validas.pop(random_value*len(validas))


        for gasolinera in gasolineras:
            for peticion in gasolinera:

    if operador == 1: # AddOnlyTrip
    elif operador == 2: # AddMultipleTrip
    
    else: # RemoveTrip

    camiones = estado._copy_camiones()
    gasolineras = [list(gasolinera) for gasolinera in estado.current_state]
    for idx_gasolinera, gasolinera in enumerate(gasolineras):
        for idx_peticio in range(len(gasolinera)):
            if gasolinera[idx_peticio] is None:
                for idx_gasolinera2, gasolinera2 in enumerate(gasolineras):
                    for idx_peticio2 in range(len(gasolinera2)):
                        if gasolinera2[idx_peticio2] is None and (idx_gasolinera != idx_gasolinera2 or idx_peticio != idx_peticio2):
                            for idx_camio, camio in enumerate(camiones):
                                distancia = estado._dist_c_g(idx_camio, idx_gasolinera)
                                km = distancia*2
                                km2 = distancia + estado._dist_c_g(idx_gasolinera, idx_gasolinera2) + estado._dist_c_g(idx_camio, idx_gasolinera2)                            
                                if estado.km_camiones[idx_camio]+km2 < MAX_KM and len(camio) < 2 * MAX_VIAJES:
#  AddOnlyTrip                                
                                    yield AddOnlyTrip(km, idx_gasolinera, idx_peticio, idx_camio)
# AddMultipleTrip 
                                    yield AddMultipleTrip(km2, idx_gasolinera, idx_gasolinera2, idx_peticio, idx_peticio2, idx_camio)                          
                                elif estado.km_camiones[idx_camio]+km < MAX_KM and len(camio) < 2 * MAX_VIAJES:
                                    yield AddOnlyTrip(km, idx_gasolinera, idx_peticio, idx_camio)                           
# RemoveTrip
                                if len(camio) > 0: # mirem si el camio té algun viatge
                                    for idx_tupla in range(0, len(camio), 2): # Vamos de 2 en 2 pues cada viaje esta formado por 2 tuplas y con estos operadores la primera siempre será not None
                                        tupla = camio[idx_tupla]
                                        tupla2 = camio[idx_tupla+1] if camio[idx_tupla+1] is not None else None
                                        idx_g = tupla[0] #  Posem idx_g per referir-nos a l'índex de la benzinera per no reescriure idx_gasolinera, no volem possibles bugs (no crec que passi res però per si de cas)
                                        idx_p = tupla[1] #  Igual que amb la benzinera
                                        distancia = estado._dist_c_g(idx_camio, idx_g)
                                        km = distancia*2
                                        if tupla2 is not None:
                                            idx_g2 = tupla2[0]
                                            idx_p2 = tupla2[1]
                                            km2 = distancia + estado._dist_c_g(idx_g, idx_g2) + estado._dist_c_g(idx_camio, idx_g2)
                                        else:
                                            idx_g2 = None
                                            idx_p2 = None
                                            yield RemoveTrip(km, idx_camio, idx_tupla, idx_g, idx_p, idx_g2, idx_p2)

#_______________________________________________________________________________________________________________
#  Apply Action
def apply_action_1(estado, action: GasOperators):
    new_state = estado.copy()
    delta_perdida = 0
    delta_beneficio = 0

    if isinstance(action, RemoveTrip):
        #  Parámetros del operador:
        idx_gasolinera1 = action.idx_gasolinera1
        idx_peticio1 = action.idx_peticio1
        idx_gasolinera2 = action.idx_gasolinera2
        idx_peticio2 = action.idx_peticio2
        
        #  Actualizamos pérdida por la petición 1:
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[idx_gasolinera1][idx_peticio1]
        delta_perdida += beneficio_hoy - beneficio_sig
        delta_beneficio += -beneficio_hoy
        #  Eliminamos la asignación de la petición 1 del current state
        new_state.current_state[idx_gasolinera1][idx_peticio1] = None
        
        #  Actualizamos pérdida por la petición 2, si hay:
        if idx_gasolinera2 is None and idx_peticio2 is None:
            beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[idx_gasolinera2][idx_peticio2]
            delta_perdida += beneficio_hoy - beneficio_sig
            delta_beneficio += -beneficio_hoy
            #  Eliminamos la asignación de la petición 2 del current state
            new_state.current_state[idx_gasolinera2][idx_peticio2] = None
        
        idx_camio = action.idx_camio
        idx_trip = action.idx_stop1
        km = action.km
        #  Eliminamos el viaje del camión 
        del new_state.camiones[idx_camio][idx_trip+1]
        del new_state.camiones[idx_camio][idx_trip]
        new_state.camiones[idx_camio][0] 
        new_state.km_camiones[idx_camio] -= km

    elif isinstance(action, AddOnlyTrip):
        #  Parámetros del operador:
        idx_gasolinera = action.idx_gasolinera
        idx_peticio = action.idx_peticio
        idx_camio = action.idx_camio
        km = action.km

        #  Actualizamos beneficio y pérdida
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[idx_gasolinera][idx_peticio]
        delta_perdida += -(beneficio_hoy - beneficio_sig)
        delta_beneficio += beneficio_hoy

        #  Creamos la asignación
        new_state.current_state[idx_gasolinera][idx_peticio] = True
        new_state.camiones[idx_camio].append((idx_gasolinera, idx_peticio))
        new_state.camiones[idx_camio].append(None)
        new_state.km_camiones[idx_camio] += km

    elif isinstance(action, AddMultipleTrip):
        #  Parámetros del operador:
        idx_gasolinera1 = action.idx_gasolinera1
        idx_peticio1 = action.idx_peticio1
        idx_gasolinera2 = action.idx_gasolinera2
        idx_peticio2 = action.idx_peticio2
        idx_camio = action.idx_camio
        km = action.km

        #  Actualizamos pérdida y beneficio:
        beneficio_hoy1, beneficio_sig1 = new_state.beneficio_peticiones[idx_gasolinera1][idx_peticio1]
        beneficio_hoy2, beneficio_sig2 = new_state.beneficio_peticiones[idx_gasolinera2][idx_peticio2]
        delta_perdida += -(beneficio_hoy1 - beneficio_sig1) + -(beneficio_hoy2 - beneficio_sig2)
        delta_beneficio += beneficio_hoy1 + beneficio_hoy2

        #  Creamos la asignación
        new_state.current_state[idx_gasolinera1][idx_peticio1] = True
        new_state.current_state[idx_gasolinera2][idx_peticio2] = True
        new_state.camiones[idx_camio].append((idx_gasolinera1, idx_peticio1))
        new_state.camiones[idx_camio].append((idx_gasolinera2, idx_peticio2))
        new_state.km_camiones[idx_camio] += km

    new_state.beneficio += delta_beneficio
    new_state.perdida_no_asignadas += delta_perdida
    return new_state
