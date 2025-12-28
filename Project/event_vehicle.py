import trafficSimulator as ts
import random

class EventVehicle(ts.Vehicle):
    def __init__(self, config={}):
        super().__init__(config)
        self.event_type = config.get('event_type', 'accident')
        self.duration = config.get('duration', 10) # seconds
        self.time_elapsed = 0 
        self.v = 0 #stopped
        self.stopped = True

        #obu properties for window display
        self.engine_type = 'obstacle'
        self.co2_emissions = 0
        self.engine_rpm = 0
        self.ac_temperature = 0
        self.DaytimeRunningLights = False
        self.windshield_wipers = False

    def update(self, lead, dt):
        self.time_elapsed += dt #duration of event
        #keep it stopped
        self.v = 0
        self.a = 0
