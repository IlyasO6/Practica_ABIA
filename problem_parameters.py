
class ProblemParameters(object):
    def __init__(self, n_distribution_centers: int, n_gas_stations: int, multiplicitat: int):
        self.n_centers = n_distribution_centers
        self.n_gas = n_gas_stations
        self.multiplicitat = multiplicitat
    def __repr__(self):
        return f"Parametros: {self.n_centros} centros de distribucion, {self.n_gas} gasolineras."