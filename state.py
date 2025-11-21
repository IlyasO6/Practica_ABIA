from __future__ import annotations
import random

# Importamos cosas necesarias para que el programa funcione.
# typing nos ayuda a decir qué tipo de datos usamos (listas, tuplas, etc.)
from typing import Dict, List, Tuple
# Importamos cosas de otros archivos que hemos creado
from abia_Gasolina import *
from problem_parameters import ProblemParameters
from operators import *

class StateRepresentation(object):
    """
    Esta clase es como una foto de cómo están las cosas en un momento dado.
    Guarda información sobre qué camiones llevan gasolina a qué gasolineras.
    """
    
    # Estas son reglas del juego que no cambian (constantes)
    MAX_KM = 640  # Lo máximo que puede recorrer un camión
    COST_KM = 2   # Cuánto cuesta moverse un kilómetro
    MAX_VIAJES = 5 # Máximo de viajes que puede hacer un camión
    MAX_PETICIONES_VIAJE = 2 # Máximo de pedidos que caben en un viaje
    
    # Aquí guardaremos las distancias y beneficios calculados para no repetirlos
    dists = None
    dists_gasolineras = None
    beneficio_peticiones = None
    lista_peticiones = None

    def __init__(self, 
                 asignaciones: List[List[int],],
                 camiones:list[list[Tuple,],],
                 km_camiones:list,
                 beneficio:float, 
                 distancia_total:float,
                 perdida_no_asignadas:float,
                 pasos:int=0):    
        # Aquí guardamos toda la información de este estado
        self.current_state = asignaciones # Qué camión atiende cada petición
        self.camiones = camiones # La ruta de cada camión
        self.km_camiones = km_camiones # Cuántos km ha recorrido cada camión
        self.beneficio = beneficio # Cuánto dinero ganamos
        self.distancia = distancia_total # Distancia total recorrida por todos
        self.perdida_no_asignadas = perdida_no_asignadas # Dinero perdido por no atender peticiones
        self.pasos = pasos # Cuántos pasos hemos dado
    
    def copy(self):
        """ 
        Crea una copia exacta de este estado. 
        Es como sacar una fotocopia para poder pintar encima sin estropear el original.
        """
        new_state = StateRepresentation(
            asignaciones= [list(gasolinera) for gasolinera in self.current_state],
            camiones= [camion.copy() for camion in self.camiones],
            km_camiones= self.km_camiones.copy(),
            beneficio= self.beneficio,
            distancia_total=self.distancia,
            perdida_no_asignadas= self.perdida_no_asignadas,
            pasos = self.pasos
        )
        return new_state

    def __repr__(self) -> str:
        """ 
        Esto sirve para que cuando imprimamos el estado, se vea bonito y entendible.
        Nos cuenta la historia de qué está pasando en cada gasolinera y camión.
        """
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
        """ 
        Prepara los datos antes de empezar.
        Calcula todas las distancias entre lugares y cuánto dinero da cada petición.
        Así no tenemos que calcularlo una y otra vez.
        """
        matriu_distancies = list() # Matriz de distancias Centro -> Gasolinera
        matriu_distancies_gasolineres = list() # Matriz de distancias Gasolinera -> Gasolinera
        
        # Calculamos distancias para cada gasolinera
        for gasolinera_coord in gasolineras:
            row = list()
            row2 = list()
            # Distancia desde cada centro a esta gasolinera
            for centro_coord in centros:
                distancia = abs(centro_coord[0] - gasolinera_coord[0]) + abs(centro_coord[1] - gasolinera_coord[1])
                row.append(distancia)
            
            # Distancia desde otras gasolineras a esta gasolinera
            for gasolinera_coord2 in gasolineras:
                distancia = abs(gasolinera_coord2[0] - gasolinera_coord[0]) + abs(gasolinera_coord2[1] - gasolinera_coord[1])
                row2.append(distancia)
            
            matriu_distancies.append(row)
            matriu_distancies_gasolineres.append(row2)
        
        # Guardamos las matrices calculadas en la clase
        cls.dists = matriu_distancies #  matriz centros y gasolineras
        cls.dists_gasolineras = matriu_distancies_gasolineres # matriz de gasolineras y gasolineras

        # Calculamos cuánto dinero da cada petición
        llista_benefici = list()
        for i in range (len(gasolineras)):
            benefici_gasolinera = list()
            for peticion in peticiones[i]:
                # Calculamos el precio según los días que lleva esperando
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
    def _dist_c_g(cls, camion_id: int, gas_id: int) -> int:
        # Nos dice la distancia entre un camión (en su centro) y una gasolinera
        return cls.dists[gas_id][camion_id]
    @classmethod
    def _dist_g_g(cls, g1: int, g2: int) -> int:
        # Nos dice la distancia entre dos gasolineras
        return cls.dists_gasolineras[g1][g2]

    @classmethod
    def _distancia_ruta(cls, camion_id: int, ruta: List[Tuple[int, int]]) -> int:
        """ 
        Calcula cuántos kilómetros recorre un camión si sigue una ruta específica.
        Suma los viajes de ida y vuelta al centro.
        """
        distancia = 0
        #  si ruta == [] -> ruta = False
        #  si ruta tiene un valor != False, any(ruta) = True
        if ruta and any(ruta):
            n = len(ruta) 
            # Miramos los viajes de dos en dos (porque un viaje puede tener hasta 2 paradas)
            for idx_posicion in range(0, n, 2):
                p1 = ruta[idx_posicion]
                # Miramos si hay una segunda parada en este viaje
                p2 = ruta[idx_posicion + 1] if idx_posicion + 1 < n else None
                
                # Si no hay paradas en este viaje, pasamos al siguiente
                if p1 is None and p2 is None:
                    continue

                # Si hay dos paradas: Centro -> Gasolinera 1 -> Gasolinera 2 -> Centro
                if p1 is not None and p2 is not None:
                    g1 = p1[0]
                    g2 = p2[0]
                    distancia += (
                        cls._dist_c_g(camion_id, g1) +
                        cls._dist_g_g(g1, g2) +
                        cls._dist_c_g(camion_id, g2)
                    )
                # Si solo hay una parada: Centro -> Gasolinera -> Centro
                else:
                    g = (p1 or p2)[0] # Cogemos la que no sea None
                    distancia += cls.COST_KM * cls._dist_c_g(camion_id, g)
        return distancia


    def generate_actionsx(self):
        """
        Esta función piensa en TODOS los posibles cambios que podemos hacer.
        Es como probar todas las llaves para ver cuál abre la puerta.
        Genera acciones para: quitar peticiones, moverlas, intercambiarlas o añadir nuevas.
        """
        camiones = self.camiones
        #  enumerate: devuelve (indice, elemento)
        #  entonces: idx_camion, camion = (indice_camion, camion[indice_camion])
        for idx_camion, camion in enumerate(camiones):
            for idx_posicion in range(len(camion)):
                #  para ver la distancia anterior (la actual) accedemos a la lista de km_camiones
                distancia_anterior1 = self.km_camiones[idx_camion]
                
                # Si hay una petición en esta posición, probamos a quitarla o moverla
                if len(camion) > 0 and camion[idx_posicion] is not None:
                    # 1. Probar a QUITAR la petición (RemovePetition)
                    copia_camion = camion.copy() #  creamos una copia para hacer el prototipo
                    copia_camion[idx_posicion] = None #  eliminamos la peticion en la copia
                    #  calculamos la distancia DESPUES de eliminar la peticion
                    distancia_posterior1 = self._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                    #  calculamos la diferencia de distancias entre la lista actual y la modificada
                    diferencia_dist = distancia_posterior1 - distancia_anterior1
                    #  devolvemos en el generador el operador RemovePetition
                    yield RemovePetition(idx_camion=idx_camion, idx_posicion=idx_posicion, 
                                        diferencia_dist= diferencia_dist)
                    
                    # 2. Probar a MOVER la petición a otro camión (MovePetition)
                    for idx_camion2, camion2 in enumerate(camiones):
                        if idx_camion == idx_camion2:
                            continue # No la movemos al mismo camión
                        distancia_anterior2 = self.km_camiones[idx_camion2]
                        # Probamos a ponerla en cualquier posición del otro camión
                        for idx_posicion2 in range(len(camion2) + 1):
                            copia_camion = camion2.copy()
                            copia_camion.insert(idx_posicion2, camion[idx_posicion])
                            
                            # Si cabe en el camión (no supera viajes máximos)
                            if len(copia_camion) < 2 * self.MAX_VIAJES:
                                distancia_posterior2 = self._distancia_ruta(camion_id = idx_camion2, ruta = copia_camion)
                                diferencia_dist2 = distancia_posterior2 - distancia_anterior2
                                # Si no se pasa de kilómetros máximos
                                if distancia_posterior2 < self.MAX_KM:
                                    yield MovePetition(idx_posicion1=idx_posicion, idx_posicion2=idx_posicion2,
                                                    idx_camion1=idx_camion, idx_camion2=idx_camion2,
                                                    diferencia_dist1= diferencia_dist,
                                                    diferencia_dist2= diferencia_dist2)
                
                # 3. Probar a INTERCAMBIAR dos peticiones dentro del mismo camión (IntraSwap)
                for idx_posicion2 in range(len(camion)):
                    if idx_posicion != idx_posicion2:
                        copia_camion = camion.copy()
                        # Hacemos el cambio
                        copia_camion[idx_posicion] = camion[idx_posicion2]
                        copia_camion[idx_posicion2] = camion[idx_posicion]
                        
                        distancia_posterior1 = self._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                        diferencia_dist = distancia_posterior1 - distancia_anterior1
                        if distancia_posterior1 < self.MAX_KM:
                            yield IntraSwap(idx_camion=idx_camion, idx_posicion1=idx_posicion, idx_posicion2=idx_posicion2,
                                            diferencia_dist= diferencia_dist)
        
        # 4. Probar a ASIGNAR peticiones que no tienen camión (AssignPetition)
        for idx_gasolinera in range(len(self.current_state)):
            for idx_peticion in range(len(self.current_state[idx_gasolinera])):
                # Si la petición no está asignada (es None)
                if self.current_state[idx_gasolinera][idx_peticion] is None:
                    for idx_camion, camion in enumerate(camiones):
                        if len(camion) < 2 * self.MAX_VIAJES:
                            distancia_anterior1 = self.km_camiones[idx_camion]
                            # Probamos a ponerla en cualquier hueco del camión
                            for idx_posicion in range(len(camion) + 1):

                                #  camion = lista, la lista representa la ruta, camiones = [[(1,2), None, None], [None, (0, 0)]]
                                copia_camion = camion.copy()
                                copia_camion.insert(idx_posicion, (idx_gasolinera, idx_peticion))
                                distancia_posterior1 = self._distancia_ruta(camion_id = idx_camion, ruta = copia_camion)
                                diferencia_dist = distancia_posterior1 - distancia_anterior1
                                if distancia_posterior1 < self.MAX_KM:
                                    yield AssignPetition(idx_gasolinera=idx_gasolinera, idx_peticion=idx_peticion, 
                                                        idx_camion=idx_camion, idx_posicion=idx_posicion,
                                                        diferencia_dist= diferencia_dist)

    def generate_one_actionx(self):
        """
        Esta función elige UNA sola acción al azar.
        Es como tirar un dado para decidir qué cambio hacer.
        """
        camiones = self.camiones
        n_camiones = len(camiones)
        idxs_camion = list(range(n_camiones))
        
        def km(camion_id, ruta=None):
            r = self.camiones[camion_id] if ruta is None else ruta
            return self._distancia_ruta(camion_id=camion_id, ruta=r)
        
        def assign():
            """ Intenta asignar una petición libre a un camión """
            libres = [(g, p)
                    for g in range(len(self.current_state))
                    for p in range(len(self.current_state[g]))
                    if self.current_state[g][p] is None]

            if not libres:
                return None
            
            random.shuffle(libres)

            random.shuffle(idxs_camion)
            for g, p in libres:
                for idx_camion in idxs_camion:
                    ruta = camiones[idx_camion]
                    if len(ruta) < 2 * self.MAX_VIAJES:
                        pos = random.randrange(len(ruta) + 1)
                        copia_ruta = ruta.copy()
                        copia_ruta.insert(pos, (g,p))
                        distancia_anterior = self.km_camiones[idx_camion]
                        distancia_posterior = self._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)

                        if distancia_posterior <= self.MAX_KM:
                            return AssignPetition(
                                idx_gasolinera= g,
                                idx_peticion=p,
                                idx_camion=idx_camion,
                                idx_posicion=pos,
                                diferencia_dist= distancia_posterior - distancia_anterior
                            )
            return None
        def move():
            """ Intenta mover una petición de un camión a otro """
            candidatos = [(idx_camion, idx_posicion)
                    for idx_camion, ruta in enumerate(self.camiones)
                    for idx_posicion in range(len(ruta))
                    if ruta and ruta[idx_posicion] is not None]
            random.shuffle(candidatos)
            for idx_camion1, idx_posicion1 in candidatos:
                peticion = self.camiones[idx_camion1][idx_posicion1]
                ruta1 = self.camiones[idx_camion1]
                ruta1_post = ruta1.copy()

                ruta1_post[idx_posicion1] = None
                distancia_anterior1 = self.km_camiones[idx_camion1]
                distancia_posterior1 = self._distancia_ruta(camion_id=idx_camion1, ruta=ruta1_post)
                diferencia_distancia1 = distancia_posterior1 - distancia_anterior1


                random.shuffle(idxs_camion)
                for idx_camion2 in idxs_camion:
                    if idx_camion2 == idx_camion1:
                        continue
                    ruta2 = self.camiones[idx_camion2]
                    if len(ruta2) < 2 * self.MAX_VIAJES:
                        
                        pos2 = random.randrange(len(ruta2) + 1)
                        ruta2_post = ruta2.copy()
                        ruta2_post.insert(pos2, peticion)
                        distancia_anterior2 = self.km_camiones[idx_camion2]
                        distancia_posterior2 = self._distancia_ruta(camion_id=idx_camion2, ruta=ruta2_post)
                        if distancia_posterior2 <= self.MAX_KM:
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
            """ Intenta intercambiar dos peticiones dentro del mismo camión """
            random.shuffle(idxs_camion)
            for idx_camion in idxs_camion:
                ruta = self.camiones[idx_camion]
                pos_validas = [i for i, x in enumerate(ruta) if x is not None]
                if len(pos_validas) < 2:
                    continue
                i, j = random.sample(pos_validas, 2)
                copia_ruta = ruta.copy()
                copia_ruta[i], copia_ruta[j] = copia_ruta[j], copia_ruta[i]
                distancia_posterior = self._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)
                if distancia_posterior <= self.MAX_KM:
                    return IntraSwap(
                        idx_camion=idx_camion,
                        idx_posicion1=i,
                        idx_posicion2=j,
                        diferencia_dist=distancia_posterior - km(idx_camion, ruta)
                    )
            return None

        def remove():
            """ Intenta quitar una petición de un camión """
            candidatos = [(idx_camion, idx_posicion)
                    for idx_camion, ruta in enumerate(camiones)
                    for idx_posicion in range(len(ruta))
                    if ruta and ruta[idx_posicion] is not None]
            if candidatos:
                idx_camion, idx_posicion = random.choice(candidatos)
                ruta = self.camiones[idx_camion]
                copia_ruta = ruta.copy()
                # si tu apply_actionx elimina con pop, usa pop aquí también
                copia_ruta[idx_posicion] = None
                distancia_posterior = self._distancia_ruta(camion_id=idx_camion, ruta=copia_ruta)
                return RemovePetition(
                    idx_posicion=idx_posicion,
                    idx_camion=idx_camion,
                    diferencia_dist=distancia_posterior - self.km_camiones[idx_camion]
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
        return []


    def apply_actionx(self, action):
        """
        Esta función aplica un cambio al estado actual y devuelve el nuevo estado.
        Es como mover una pieza en el tablero y ver cómo queda la partida.
        """
        new_state = self.copy()
        delta_beneficio, delta_perdida = 0,0
        
        # Si la acción es ASIGNAR una petición
        if isinstance(action, AssignPetition): #  si action es instancia de AssignPetition
            #  Marca en la peticion de la gasolinera idx_gasolinera que esta asignada (True):
            new_state.current_state[action.idx_gasolinera][action.idx_peticion] = True
            #  añade la peticion al camion
            new_state.camiones[action.idx_camion].insert(action.idx_posicion, (action.idx_gasolinera, action.idx_peticion))

            #  actualiza el beneficio:
            beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[action.idx_gasolinera][action.idx_peticion]
            delta_beneficio = beneficio_hoy
            delta_perdida = -(beneficio_hoy - beneficio_sig)
            
            #  actualiza la distancia global y la del camion respectivo:
            new_state.km_camiones[action.idx_camion] += action.diferencia_dist
            new_state.distancia += action.diferencia_dist

        # Si la acción es MOVER una petición de un camión a otro
        elif isinstance(action, MovePetition):
            peticion = new_state.camiones[action.idx_camion1][action.idx_posicion1]

            #  añade la peticion al camion 2:
            new_state.camiones[action.idx_camion2].insert(action.idx_posicion2, peticion)
            #  y la borra del camion 1:
            new_state.camiones[action.idx_camion1].pop(action.idx_posicion1)

            #  actualiza distancias camion 1 y camion 2:
            new_state.km_camiones[action.idx_camion1] += action.diferencia_dist1
            new_state.km_camiones[action.idx_camion2] += action.diferencia_dist2

            #  actualiza la distancia global
            new_state.distancia += action.diferencia_dist1 + action.diferencia_dist2

        # Si la acción es QUITAR una petición
        elif isinstance(action, RemovePetition):
            gasolinera, peticion = new_state.camiones[action.idx_camion][action.idx_posicion]
            new_state.current_state[gasolinera][peticion] = None
            new_state.camiones[action.idx_camion][action.idx_posicion] = None

            beneficio_hoy, beneficio_sig = new_state.beneficio_peticiones[gasolinera][peticion]
            delta_beneficio = -beneficio_hoy
            delta_perdida = beneficio_hoy - beneficio_sig

            new_state.km_camiones[action.idx_camion] += action.diferencia_dist
            new_state.distancia += action.diferencia_dist

        # Si la acción es INTERCAMBIAR dos peticiones en el mismo camión
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


def generate_initial_state_empty(params):
    """
    Crea un estado inicial vacío.
    Es como empezar con el tablero limpio: ningún camión lleva nada.
    """
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000)
    print("Params:", n_gas, n_centers, multiplicitat, seed, sep="\n")
    
    # Creamos las gasolineras y sus peticiones
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    # Inicializamos el estado de las gasolineras (todo vacío/None)
    gas_stations = [[None for _ in row] for row in peticiones] 
    #  Los índices de las gasolineras coinciden con los de la lista de Gasolineras 
    #  Inicialmente no hay camión que haya satisfecho las peticiones
    #  Una vez esten satisfechas se cambiará None por el índice del camión que la haya satisfecho
    
    # Obtenemos coordenadas
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
        CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
    
    # Inicializamos camiones vacíos
    camions = [[] for _ in centros_coords]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion
    km_camiones = [0 for _ in centros_coords]
    
    # Precalculamos distancias y beneficios
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    # Calculamos la pérdida inicial (todo lo que dejamos de ganar por no atender nada)
    perdida_total = 0
    for gas in range(len(gas_stations)):
        for pet in (range(len(gas_stations[gas]))):
            beneficio_hoy, beneficio_sig = StateRepresentation.beneficio_peticiones[gas][pet]
            perdida_total += beneficio_hoy - beneficio_sig
            
    StateRepresentation.MAX_KM = params.max_km
    StateRepresentation.COST_KM = params.cost_km
    
    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camions,
        km_camiones=km_camiones, 
        beneficio=0,
        distancia_total=0,
        perdida_no_asignadas=perdida_total,
    )


def generate_initial_state_random(params: ProblemParameters, seed: int | None = None):
    """
    Crea un estado inicial aleatorio válido:
    - Asigna peticiones a camiones respetando:
        * Máx. viajes por camión (MAX_VIAJES => 2 slots por viaje)
        * Máx. kilómetros por camión (MAX_KM)
    - Cada viaje ocupa 2 posiciones en la ruta: [(g1,p1),(g2,p2)] o [(g1,p1), None]
    - Evita emparejar dos peticiones de la misma gasolinera en el mismo viaje.
    """
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat

    rng = random.Random(seed if seed is not None else random.randint(0, 10_000))

    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=rng.randint(0, 10_000)).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]

    # current_state: None si no asignada; cuando asignada, contiene el idx del camión
    gas_stations = [[None for _ in row] for row in peticiones]

    gasolineras_coords = [(g.cx, g.cy) for g in gasolineras]
    centros_coords = [(c.cx, c.cy) for c in CentrosDistribucion(
        num_centros=n_centers, multiplicidad=multiplicitat, seed=rng.randint(0, 10_000)
    ).centros]

    # Precompute distances and benefits
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    # Inicializar rutas vacías
    camiones = [[] for _ in centros_coords]

    # Pool de peticiones sin asignar
    pool = [(g, p) for g in range(len(peticiones)) for p in range(len(peticiones[g]))]
    rng.shuffle(pool)

    beneficio_total = 0.0

    # Intentamos añadir viajes (hasta que no sea posible añadir más)
    made_progress = True
    while pool and made_progress:
        made_progress = False
        cam_ids = list(range(len(centros_coords)))
        rng.shuffle(cam_ids)

        for cid in cam_ids:
            ruta = camiones[cid]
            if len(ruta) >= 2 * StateRepresentation.MAX_VIAJES:
                continue

            # Intentos por camión en esta pasada (evita ciclos infinitos)
            attempts = min(20, len(pool))
            for _ in range(attempts):
                if not pool:
                    break

                # Elegimos una petición base
                g1, p1 = pool[rng.randrange(len(pool))]

                # Candidatos para segunda parada (no misma gasolinera)
                candidates2 = [(g2, p2) for (g2, p2) in pool if not (g2 == g1 and p2 == p1) and g2 != g1]
                rng.shuffle(candidates2)

                # Probar primero con dos paradas (si hay candidatos), luego con 1
                tried_variants = []

                if candidates2:
                    # Limitar intentos de pareja para no explorar todo
                    k2 = min(10, len(candidates2))
                    for (g2, p2) in candidates2[:k2]:
                        viaje = [(g1, p1), (g2, p2)]
                        copia = ruta + viaje
                        km_total = StateRepresentation._distancia_ruta(camion_id=cid, ruta=copia)
                        if km_total <= StateRepresentation.MAX_KM and len(copia) <= 2 * StateRepresentation.MAX_VIAJES:
                            # Aceptar 2 paradas
                            ruta.extend(viaje)
                            camiones[cid] = ruta
                            gas_stations[g1][p1] = cid
                            gas_stations[g2][p2] = cid
                            beneficio_total += StateRepresentation.beneficio_peticiones[g1][p1][0]
                            beneficio_total += StateRepresentation.beneficio_peticiones[g2][p2][0]
                            # Eliminar del pool
                            pool.remove((g1, p1))
                            pool.remove((g2, p2))
                            made_progress = True
                            break
                        tried_variants.append(("2stop", (g1, p1, g2, p2)))

                    if made_progress:
                        break

                # Si 2 paradas no fue posible, probamos 1 parada
                viaje = [(g1, p1), None]
                copia = ruta + viaje
                km_total = StateRepresentation._distancia_ruta(camion_id=cid, ruta=copia)
                if km_total <= StateRepresentation.MAX_KM and len(copia) <= 2 * StateRepresentation.MAX_VIAJES:
                    ruta.extend(viaje)
                    camiones[cid] = ruta
                    gas_stations[g1][p1] = cid
                    beneficio_total += StateRepresentation.beneficio_peticiones[g1][p1][0]
                    pool.remove((g1, p1))
                    made_progress = True
                    break

            # Si este camión no pudo añadir nada, pasamos al siguiente
            # Continuamos el bucle for cid

    # Recalcular km y distancia total coherente con la representación final
    km_camiones = [StateRepresentation._distancia_ruta(camion_id=i, ruta=camiones[i])
                   for i in range(len(camiones))]
    distancia_total = sum(km_camiones)

    # Pérdida de no asignadas = suma(beneficio_hoy - beneficio_sig) de todas las no asignadas
    perdida_total = 0.0
    for g in range(len(gas_stations)):
        for p in range(len(gas_stations[g])):
            if gas_stations[g][p] is None:
                beneficio_hoy, beneficio_sig = StateRepresentation.beneficio_peticiones[g][p]
                perdida_total += (beneficio_hoy - beneficio_sig)
    StateRepresentation.MAX_KM = params.max_km
    StateRepresentation.COST_KM = params.cost_km

    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camiones,
        km_camiones=km_camiones,
        beneficio=beneficio_total,
        distancia_total=distancia_total,
        perdida_no_asignadas=perdida_total
    )


def generate_initial_state_greedy(params: ProblemParameters, seed = None):
    """
    Crea un estado inicial "codicioso" (greedy).
    Intenta hacerlo lo mejor posible paso a paso, sin mirar muy lejos en el futuro.
    1. Agrupa gasolineras por cercanía a los centros.
    2. Asigna las peticiones más valiosas primero.
    """
    n_centers = params.n_centers
    n_gas = params.n_gas
    multiplicitat = params.multiplicitat
    seed = random.randint(0, 10000) if seed== None else seed
    gasolineras = Gasolineras(num_gasolineras=n_gas, seed=seed).gasolineras
    peticiones = [gasolinera.peticiones for gasolinera in gasolineras]
    
    gas_stations = [[None for _ in row] for row in peticiones] 
    
    gasolineras_coords = [(gasolinera.cx, gasolinera.cy) for gasolinera in gasolineras]
    centros_coords = [(centro.cx, centro.cy) for centro in 
    CentrosDistribucion(num_centros=n_centers, multiplicidad=multiplicitat, seed=seed).centros]
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

    # 1. Agrupar gasolineras (Clusters)
    # Cada gasolinera se asigna al centro de distribución más cercano
    clusters = []
    #  cada numero representa el cluster al que esta asignada la gasolinera del indice del numero
    #  
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
    
    # 2. Asignar peticiones a camiones
    for id_camion in range(len(centros_coords)):

        # Recogemos todas las peticiones de las gasolineras cercanas a este centro
        peticiones_cluster = []

        for id_gasolinera, id_cluster in enumerate(clusters):
            if id_cluster == id_camion:
                for id_peticion, dias in enumerate(peticiones[id_gasolinera]):
                    porcentaje = max(0, 100 - 2**dias) / 100 if dias > 0 else 1.02
                    beneficio = 1000 * porcentaje
                    peticiones_cluster.append((beneficio, id_gasolinera, id_peticion))
        
        #  Las ordenamos por beneficio (las que dan más dinero primero) 

        
        peticiones_cluster.sort(reverse=True, key = lambda x: x[0])

        km = 0
        num_viajes = 0
        peticiones_asignadas = set()

        # Llenamos el camión hasta que no quepa más o no haya peticiones
        while peticiones_cluster and num_viajes < 5:
            peticion_actual = None

            # Buscamos la primera petición no asignada
            for pet in peticiones_cluster:
                if (pet[1], pet[2]) not in peticiones_asignadas:
                    peticion_actual = pet
                    break
            
            if peticion_actual is None: break

            beneficio1, gas1, pet1 = peticion_actual
            
            # Buscamos una segunda petición para completar el viaje (si se puede)
            beneficio2, gas2, pet2 = 0, None, None
            min_dist = float('inf')

            for pet in peticiones_cluster:
                # Que no esté asignada y que no sea de la misma gasolinera
                if (pet[1], pet[2]) not in peticiones_asignadas and pet[1] != gas1:
                    dist = StateRepresentation.dists_gasolineras[gas1][pet[1]]

                    # Buscamos la más cercana a la primera gasolinera
                    if dist < min_dist:
                        min_dist = dist
                        beneficio2, gas2, pet2 = pet
        
            # Creamos el viaje (con 1 o 2 paradas)
            if gas2 is not None:
                viaje = [(gas1, pet1), (gas2, pet2)]
            else:
                viaje = [(gas1, pet1), None]
            
            # Comprobamos si el viaje es válido (distancia máxima)
            copia_camion = camiones[id_camion].copy()
            copia_camion.extend(viaje)
            km_viaje = StateRepresentation._distancia_ruta(camion_id=id_camion,
                                                           ruta=copia_camion)
            
            if km_viaje <= params.max_km:
                # Si es válido, lo añadimos definitivamente
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
                # Si nos pasamos de km, paramos de llenar este camión
                break
    
    # Calculamos pérdidas
    perdida_total = 0
    for gas in range(len(gas_stations)):
        for pet in (range(len(gas_stations[gas]))):
            if gas_stations[gas][pet] == None:
                beneficio_hoy, beneficio_sig = StateRepresentation.beneficio_peticiones[gas][pet]
                perdida_total += beneficio_hoy - beneficio_sig
    print(beneficio_total, perdida_total, distancia_total)
    StateRepresentation.MAX_KM = params.max_km
    StateRepresentation.COST_KM = params.cost_km
    return StateRepresentation(
        asignaciones=gas_stations,
        camiones=camiones,
        km_camiones=km_camiones,
        beneficio=beneficio_total,
        distancia_total=distancia_total,
        perdida_no_asignadas= perdida_total
    )

