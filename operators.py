from typing import Dict, List, Tuple


class Operators(object):
    pass

class AddOnlyTrip(Operators):
    def __init__(self, gasolinera, peticio, camio, km): #los índices referenciando cada uno
        self.gasolinera = gasolinera
        self.peticio = peticio
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix petició {self.peticio} de la benzinera {self.gasolinera} i torna al centre de distribució."

class AddMultipleTrip(Operators):
    def __init__(self, gasolinera1, gasolinera2, peticio1, peticio2, camio, km):
        self.gasolinera1 = gasolinera1
        self.peticio1 = peticio1
        self.gasolinera2 =  gasolinera2
        self.peticio2 = peticio2
        self.camio = camio
        self.km = km

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."

class RemoveTrip(Operators):
    def __init__(self, camio, trip: Tuple[Tuple, Tuple], gasolinera1, peticio1, gasolinera2=None, peticio2=None, km): #  trip es la tupla que té 
        self.camio = camio
        self.trip = trip
        self.km = km
        if gasolinera2==None and peticio2==None:
            self.gasolinera = gasolinera1
            self.peticio = peticio1
        else:
            self.gasolinera1 = gasolinera1
            self.peticio1 = peticio1
            self.gasolinera2 = gasolinera2
            self.peticio2 = peticio1

    def __repr__(self) -> str:
        if self.gasolinera2==None and self.peticio2==None:
            return f"Eliminem l'assoliment de la petició {self.peticio} de la benzinera {self.gasolinera}"
        else:
            return f"Eliminem l'assoliment de les peticions: {self.peticio1} de la benzinera {self.gasolinera1} i {self.peticio2} de la benzinera {self.gasolinera2}"
        
            
        
class InterchangeTrips(Operators):
    def __init__(self, camio1, 
                 trip1: Tuple[Tuple, Tuple], 
                 gasolinera1_1, 
                 gasolinera1_2=None, 
                 peticio1_1, 
                 peticio1_2=None, 
                 camio2, 
                 trip2: Tuple[Tuple, Tuple], 
                 gasolinera2_1, 
                 gasolinera2_2=None, 
                 peticio2_1, 
                 peticio2_2=None): #  trip es la tupla que té 
        self.camio1 = camio1
        self.trip1 = trip1
        if gasolinera1_2 == None:
            self.gasolinera1 = gasolinera1_1
            self.peticio1 = peticio1_1
        else:
            self.gasolinera1_1 = gasolinera1_1
            self.peticio1_1 = peticio1_1
            self.gasolinera1_2 = gasolinera1_2
            self.peticio1_2 = peticio1_2

        self.camio2 = camio2
        self.trip2 = trip2
        if gasolinera2_2 == None:
            self.gasolinera2 = self.gasolinera2_1
            self.peticio2 = self.peticio2_1
        else:
            self.gasolinera2_1 = gasolinera2_1
            self.peticio2_1 = peticio2_1
            self.gasolinera2_2 = gasolinera2_2
            self.peticio2_2 = peticio2_2

    def __repr__(self) -> str:
            return f"Intercambiem els viatges {self.trip1} i {self.trip2} de camio {self.camio1} i {self.camio2}"
   
