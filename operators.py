


class Operators(object):
    pass


class add_only_trip(Operators):
    def __init__(self, peticio, camio):
        self.gasolinera, self.peticio = peticio
        self.camio = camio

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix petició {self.peticio} de la benzinera {self.gasolinera} i torna al centre de distribució."

class add_multiple_trip(Operators):
    def __init__(self, peticio1, peticio2, camio):
        self.gasolinera1, self.peticio1 = peticio1
        self.gasolinera2, self.peticio2 = peticio2
        self.camio = camio

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."

class remove_trip(Operators):
    def __init__(self, camio, trip):
        self.camio =
        self.gasolinera2, self.peticio2 = peticio2
        self.camio = camio

    def __repr__(self) -> str:
        return f"Camió {self.camio} assoleix la petició {self.peticio1} de la benzinera {self.gasolinera1} després assoleix la petició {self.peticio2} de la benzinera {self.gasolinera2} i torna al centre de distribució."
