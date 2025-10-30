from typing import Dict, List, Tuple


class Operators(object):
    pass

class add_only_trip(Operators):
    def __init__(self, gasolinera, peticio, camio): #los índices referenciando cada uno
        self.gasolinera = gasolinera
        self.peticio = peticio
        self.camio = camio

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix petició {self.peticio} de la benzinera {self.gasolinera} i torna al centre de distribució."

class add_multiple_trip(Operators):
    def __init__(self, gasolinera1, gasolinera2, peticio1, peticio2, camio):
        self.gasolinera1 = gasolinera1
        self.peticio1 = peticio1
        self.gasolinera2 =  gasolinera2
        self.peticio2 = peticio2
        self.camio = camio

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."

class remove_trip(Operators):
    def __init__(self, camio, trip: Tuple[Tuple, Tuple]): #  trip es la tupla que té 
        self.camio = camio
        self.trip = trip
        if len(self.trip) > 1:
            self.gasolinera1 = self.trip[0][0]
            self.peticio1 = self.trip[0][1]
            self.gasolinera2 = self.trip[1][0]
            self.peticio2 = self.trip[1][1]
        else:
            self.gasolinera = self.trip[0][0]
            self.peticio = self.trip[0][1]

    def __repr__(self) -> str:
        if len(self.trip) > 1:
            return f"Eliminem l'assoliment de les peticions: {self.peticio1} de la benzinera {self.gasolinera1} i {self.peticio2} de la benzinera {self.gasolinera2}"
        else:
            return f"Eliminem l'assoliment de la petició {self.peticio} de la benzinera {self.gasolinera}"
        
class interchange_trips(Operators):
    def __init__(self, camio1, trip1: Tuple[Tuple, Tuple], camio2, trip2: Tuple[Tuple, Tuple]): #  trip es la tupla que té 
        self.camio1 = camio1
        self.trip1 = trip1
        if len(self.trip1) > 1:
            self.gasolinera1_1 = self.trip1[0][0]
            self.peticio1_1 = self.trip1[0][1]
            self.gasolinera1_2 = self.trip1[1][0]
            self.peticio1_2 = self.trip1[1][1]
        else:
            self.gasolinera1 = self.trip1[0][0]
            self.peticio1 = self.trip1[0][1]

        self.camio2 = camio2
        self.trip2 = trip2
        if len(self.trip2) > 1:
            self.gasolinera2_1 = self.trip2[0][0]
            self.peticio2_1 = self.trip2[0][1]
            self.gasolinera2_2 = self.trip2[1][0]
            self.peticio2_2 = self.trip2[1][1]
        else:
            self.gasolinera2 = self.trip2[0][0]
            self.peticio2 = self.trip2[0][1]

    def __repr__(self) -> str:
            return f"Intercambiem els viatges {self.trip1} i {self.trip2} de camio {self.camio1} i {self.camio2}"
   
