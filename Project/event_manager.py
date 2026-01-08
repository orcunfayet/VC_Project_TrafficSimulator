import random
from event_vehicle import EventVehicle

class EventManager:
    def __init__(self, simulation):
        self.simulation = simulation
        self.events = []
        self.last_event_time = 0
        self.event_interval = 5 # spawn event every 5 seconds
        self.event_probability = 0.2 # 20% chance

    def update(self, dt):
        # remove expired events
        expired_events = [e for e in self.events if e.time_elapsed >= e.duration]
        for e in expired_events:
            self.remove_event(e)
        
        # spawn new events
        if self.simulation.t - self.last_event_time > self.event_interval:
            self.last_event_time = self.simulation.t
            if random.random() < self.event_probability:
                self.spawn_event()

    def spawn_event(self):
        if not self.simulation.segments:
            return

        # find eligible segments (exclude tram lines)
        eligible_indices = [
            i for i, seg in enumerate(self.simulation.segments) 
            if getattr(seg, 'category', 'general') != 'tram'
        ]
        
        if not eligible_indices:
            return

        # pick random segment
        segment_id = random.choice(eligible_indices)
        segment = self.simulation.segments[segment_id]
        
        # pick random position
        length = segment.get_length()
        x = random.uniform(0, length)
        
        # create event vehicle
        event_type = random.choice(['accident', 'construction', 'animal'])
        duration = random.uniform(5, 15)
        
        event = EventVehicle({
            'event_type': event_type,
            'duration': duration,
            'path': [segment_id], 
            'x': x
        })
        
        # add to simulation
        self.simulation.add_vehicle(event)
        self.events.append(event)
        
        # remove from end (where add_vehicle put it)
        if segment.vehicles[-1] == event.id:
            segment.vehicles.pop()
        
        # insert at correct position
        inserted = False
        for i, veh_id in enumerate(segment.vehicles):
            v = self.simulation.vehicles[veh_id]
            if event.x > v.x:
                segment.vehicles.insert(i, event.id)
                inserted = True
                break
        
        if not inserted:
            segment.vehicles.append(event.id)


    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)
            # remove from simulation
            if event.id in self.simulation.vehicles:
                del self.simulation.vehicles[event.id]
            
            # remove from segment
            if event.path:
                seg_id = event.path[0]
                segment = self.simulation.segments[seg_id]
                if event.id in segment.vehicles:
                    segment.vehicles.remove(event.id)
            
