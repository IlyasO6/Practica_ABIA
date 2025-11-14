from __future__ import annotations
import random

from typing import Dict, List, Tuple
from Practica_ABIA.abia_Gasolina import *
from Practica_ABIA.problem_parameters import ProblemParameters

class StateRepresentation(object):
    
    MAX_KM = 640
    COST_KM = 2
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
                 distancia_total:float,
                 perdida_no_asignadas:float,
                 pasos:int=0):    
        self.current_state = asignaciones
        self.camiones = camiones
        self.km_camiones = km_camiones
        self.beneficio = beneficio
        self.distancia = distancia_total
        self.perdida_no_asignadas = perdida_no_asignadas
        self.pasos = pasos
        self.sa_trace: List[Tuple[float, float]] = [
            (float(self.beneficio), float(self.distancia + self.perdida_no_asignadas))
        ]
    
    def copy(self):
        new_state = StateRepresentation(
            asignaciones= [list(gasolinera) for gasolinera in self.current_state],
            camiones= [camion.copy() for camion in self.camiones],
            km_camiones= self.km_camiones.copy(),
            beneficio= self.beneficio,
            distancia_total=self.distancia,
            perdida_no_asignadas= self.perdida_no_asignadas,
            pasos = self.pasos
        )
        new_state.sa_trace = self.sa_trace.copy()
        return new_state

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
    def _dist_c_g(cls, camion_id: int, gas_id: int) -> int:
        return cls.dists[gas_id][camion_id]
    @classmethod
    def _dist_g_g(cls, g1: int, g2: int) -> int:
        return cls.dists_gasolineras[g1][g2]

    @classmethod
    def _distancia_ruta(cls, camion_id: int, ruta: List[Tuple[int, int]]) -> int:
        distancia = 0
        if ruta and any(ruta):
            n = len(ruta)
            for idx_posicion in range(0, n, 2):
                p1 = ruta[idx_posicion]
                p2 = ruta[idx_posicion + 1] if idx_posicion + 1 < n else None

                if p1 is None and p2 is None:
                    continue

                if p1 is not None and p2 is not None:
                    g1 = p1[0]
                    g2 = p2[0]
                    distancia += (
                        cls._dist_c_g(camion_id, g1) +
                        cls._dist_g_g(g1, g2) +
                        cls._dist_c_g(camion_id, g2)
                    )
                else:
                    g = (p1 or p2)[0]
                    distancia += cls.COST_KM * cls._dist_c_g(camion_id, g)
        return distancia

#  state --> lista(lista(), lista())
#  state -->   list(tuple(gas, camio2, camio1))

def generate_initial_state_empty(params):
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
    
    camions = [[] for _ in centros_coords]  #  Los índices de las camions coinciden con los de la lista de CentrosDistribucion
    km_camiones = [0 for _ in centros_coords]
    StateRepresentation.preprocessament(gasolineras_coords, centros_coords, peticiones)

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

# ...existing code...

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
    camiones: list[list[Tuple[int, int] | None]] = [[] for _ in centros_coords]

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
                viaje = [(gas1, pet1), None]
            copia_camion = camiones[id_camion].copy()
            copia_camion.extend(viaje)
            km_viaje = StateRepresentation._distancia_ruta(camion_id=id_camion,
                                                           ruta=copia_camion)
            
            if km_viaje <= params.max_km:
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

