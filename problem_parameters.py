
class ProblemParameters(object):
    def __init__(self, n_distribution_centers: int, n_gas_stations: int, multiplicitat: int, cost_km = 2, max_km = 640):
        self.n_centers = n_distribution_centers
        self.n_gas = n_gas_stations
        self.multiplicitat = multiplicitat
        self.cost_km = cost_km
        self.max_km = max_km
    def __repr__(self):
        return f"Parametros: {self.n_centers} centros de distribucion, {self.n_gas} gasolineras."