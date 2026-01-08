import trafficSimulator as ts
from trafficSimulator.core.vehicle_generator import VehicleGenerator
from numpy.random import randint
import random

class CustomVehicle(ts.Vehicle):
    def __init__(self, config={}):
        self.vehicle_type = config.get('vehicle_type', 'car')
        if self.vehicle_type == 'tram':
            config['l'] = 10 # longer vehicle
        super().__init__(config)
        self.init_obu_data()

    def init_obu_data(self):
        # engine type
        if self.vehicle_type == 'tram':
             self.engine_type = 'Tram/electric'
        else:
            engine_types = ['electric', 'combustion', 'hybrid', 'hydrogen']
            self.engine_type = random.choice(engine_types)

        # ac temperature
        self.ac_temperature = random.uniform(18.0, 24.0)

        # daytime running lights status
        self.DaytimeRunningLights = random.choice([True, False])

        # windshield wipers status
        self.windshield_wipers = random.choice([True, False])

    def update(self, lead, dt):
        super().update(lead, dt)
        # update obu data
        self.v = self.v
        
class CustomVehicleGenerator(VehicleGenerator):
    def generate_vehicle(self):
        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total+1)
        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                return CustomVehicle(config)

