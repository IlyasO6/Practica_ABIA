from typing import Dict, List, Tuple

#  Operadores
class Operators(object):
    def __init__(self):
        pass

class AddOnlyTrip(Operators):
    def __init__(self, km, gasolinera, peticio, camio): #los índices referenciando cada uno
        self.gasolinera = gasolinera
        self.peticio = peticio
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix petició {self.peticio} de la benzinera {self.gasolinera} i torna al centre de distribució."

class AddMultipleTrip(Operators):
    def __init__(self, km, gasolinera1, gasolinera2, peticio1, peticio2, camio):
        self.gasolinera1 = gasolinera1
        self.peticio1 = peticio1
        self.gasolinera2 =  gasolinera2
        self.peticio2 = peticio2
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."

class RemoveTrip(Operators):
    def __init__(self, km, camio, trip: Tuple[Tuple, Tuple], gasolinera1, peticio1, gasolinera2=None, peticio2=None): #  trip es la tupla que té 
        self.camio = camio
        self.trip = trip
        self.km = km
        self.gasolinera2 = gasolinera2
        self.peticio2 = peticio2
        self.gasolinera1 = gasolinera1
        self.peticio1 = peticio1

    def __repr__(self) -> str:
        if self.gasolinera2==None and self.peticio2==None:
            return f"Eliminem l'assoliment de la petició {self.peticio1} de la benzinera {self.gasolinera1}"
        else:
            return f"Eliminem l'assoliment de les peticions: {self.peticio1} de la benzinera {self.gasolinera1} i {self.peticio2} de la benzinera {self.gasolinera2}" 

#  Generate Action
    #  AddOnlyTrip
def generate_actions_1(estado):
    camiones = estado._copy_camiones()
    gasolineras = [list(gasolinera) for gasolinera in estado.current_state]
    for gasolinera in range(len(gasolineras)):
        for peticio in range(len(gasolineras[gasolinera])):
            if gasolineras[gasolinera][peticio] is None:
                for camio in range(len(camiones)):
                    km = estado._distancia_viaje(camio, [(gasolinera, peticio)])
                    if camiones[camio][0]+km < 640 and len(camiones[camio]) < 6:
                        yield AddOnlyTrip(km, gasolinera, peticio, camio)
    # AddMultipleTrip
                for gasolinera2 in range(len(gasolineras)):
                    for peticio2 in range(len(gasolineras[gasolinera2])):
                        if gasolineras[gasolinera2][peticio2] is None and (gasolinera != gasolinera2 or peticio != peticio2):
                            for camio in range(len(camiones)):
                                km = estado._distancia_viaje(camio, [(gasolinera, peticio), (gasolinera2, peticio2)])
                                if camiones[camio][0]+km < 640 and len(camiones[camio]) < 6:
                                    yield AddMultipleTrip(km, gasolinera, gasolinera2, peticio, peticio2, camio)
    # RemoveTrip
    for camio in range(len(camiones)):
        if len(camiones[camio]) > 1: # mirem si el camio té algun viatge
            for tupla in range(1, len(camiones[camio])):
                trip = camiones[camio][tupla]
                km = estado._distancia_viaje(camio, trip)
                gasolinera = trip[0][0]
                peticio = trip[0][1]
                if len(trip) == 1:
                    yield RemoveTrip(km, camio, tupla, gasolinera, peticio)
                else:
                    gasolinera2 = trip[1][0]
                    peticio2 = trip[1][1]
                    yield RemoveTrip(km, camio, tupla, gasolinera, peticio, gasolinera2, peticio2)

#  Apply Action
def apply_action_1(estado, action: Operators):
    new_state = estado.copy()
    delta_beneficio, delta_perdida = 0,0
    if isinstance(action, RemoveTrip):
        #  Parametros del operador:
        gasolinera1 = action.gasolinera1
        peticio1 = action.peticio1
        if action.gasolinera2 and action.peticio2:
            gasolinera2 = action.gasolinera2
            peticio2 = action.peticio2
            #  Actualizamos perdida:
            beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera2][peticio2]
            delta_perdida = beneficio_hoy - beneficio_sig
            #  Eliminamos la asignación
            new_state.current_state[gasolinera2][peticio2] = None 
        camio = action.camio
        trip = action.trip
        km = action.km
        #  Actualizamos perdida:
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera1][peticio1]
        delta_perdida += beneficio_hoy - beneficio_sig
        #  Eliminamos la asignación
        new_state.current_state[gasolinera1][peticio1] = None
        del new_state.camiones[camio][trip]
        new_state.camiones[camio][0] -= km
        new_state.distancia -= km
    
    elif isinstance(action, AddOnlyTrip):
        #  Parametros del operador:
        gasolinera = action.gasolinera
        peticio = action.peticio
        camio = action.camio
        km = action.km
        #  Actualizamos beneficio y perdida
        beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera][peticio]
        delta_perdida = -(beneficio_hoy - beneficio_sig)
        delta_beneficio = beneficio_hoy
        #  Creamos la asignación
        new_state.current_state[gasolinera][peticio] = camio
        new_state.camiones[camio].append([(gasolinera, peticio)])
        new_state.camiones[camio][0] += km
        new_state.distancia += km

    elif isinstance(action, AddMultipleTrip):
        #  Parametros del operador:
        gasolinera1 = action.gasolinera1
        peticio1 = action.peticio1
        gasolinera2 = action.gasolinera2
        peticio2 = action.peticio2
        camio = action.camio
        km = action.km
        #  Actualizamos perdida y beneficio:
        beneficio_hoy1, beneficio_sig1 = new_state.beneficio_peticiones[gasolinera1][peticio1]
        beneficio_hoy2, beneficio_sig2 = new_state.beneficio_peticiones[gasolinera2][peticio2]
        delta_perdida1 = -(beneficio_hoy1 - beneficio_sig1)
        delta_beneficio1 = beneficio_hoy1
        delta_perdida2 = -(beneficio_hoy2 - beneficio_sig2)
        delta_beneficio2 = beneficio_hoy2
        delta_perdida = delta_perdida1 + delta_perdida2
        delta_beneficio = delta_beneficio1 + delta_beneficio2
        #  Creamos la asignación
        new_state.current_state[gasolinera1][peticio1] = camio
        new_state.current_state[gasolinera2][peticio2] = camio
        new_state.camiones[camio].append([(gasolinera1, peticio1), (gasolinera2, peticio2)])
        new_state.camiones[camio][0] += km
        new_state.distancia += km
        #print(f"camion: {camio}")
        #print(new_state.camiones)
    new_state.beneficio += delta_beneficio
    new_state.perdida_no_asignadas += delta_perdida
    return new_state