import trafficSimulator as ts
import dearpygui.dearpygui as dpg
from create_topology import create_golden_horn_track
from custom_window import CustomWindow
from custom_vehicle import CustomVehicleGenerator

#Implemented Functions: 

# Draw the road segments with 
# different colors and width given their category 
# (e.g., general lane, lane reserved for taxis, lane reserved for public
# transport buses, etc.) and material (e.g., asphalt, concrete, gravel, dirt, etc)
# custom_window.py achieves this.

# Add the possibility to assign a “mnemonic” identifier (i.e., a string) to the
# road segments, to simply their handling and usage during the topology
# creation.
# custom_window.py achieves this.

# Define new topologies featuring multiple segments and intersections (e.g.,
# a simplified modeling of the Scientific Campus of UNIPR, a small district
# of a real existing city, etc.).
# create_topology.py achieves this.

# Include additional informations to be ideally managed by the OBUs present
# on-board the vehicles (e.g., CO2 emissions, engine type (electric, 
# combustion, hybrid, hydrogen, etc.), engine RPM, internal A/C temperature,
# ambient light level, fog lights status, rain sensor detection, etc.).
# custom_vehicle.py achieves this.

# Define the possibility to show events (e.g., accidents, road construction
# sites, etc.) happening at certain (randomly-selected and/or scheduled)
# time instants and possibly (in the future) generating traffic congestion.
# event_manager.py and event_vehicle.py achieves this.

vg = CustomVehicleGenerator({
    'vehicles': [
        (2, {'vehicle_type': 'car', 'v': 8, 'path': [2,3,4]}),   # Car: Up
        (2, {'vehicle_type': 'car', 'v': 8, 'path': [5,6,7]}),  # Car: Down
        (1, {'vehicle_type': 'tram', 'v': 10, 'path': [0]}),          # Tram: Up
        (1, {'vehicle_type': 'tram', 'v': 10, 'path': [1]}),          # Tram: Down
    ]
})

sim = ts.Simulation()
create_golden_horn_track(sim)
sim.add_vehicle_generator(vg)
win = CustomWindow(sim)
win.run()
win.show()