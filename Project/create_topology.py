import trafficSimulator as ts

def create_segment(sim, start, end, category='general', material='asphalt', name=None, z_level=0):
    sim.create_segment(start, end)
    seg = sim.segments[-1]
    seg.category = category
    seg.material = material
    seg.z_level = z_level 
    if name:
        seg.name = name

def create_quadratic_bezier_curve(sim, start, control, end, category='general', material='asphalt', name=None, z_level=0):
    sim.create_quadratic_bezier_curve(start, control, end)
    seg = sim.segments[-1]
    seg.category = category
    seg.material = material
    seg.z_level = z_level
    if name:
        seg.name = name

def create_golden_horn_track(sim):
    
    # tram segments (inner)
    create_segment(sim, (2, -60), (2, 60), category='tram', material='concrete', name='Up Tram') # 0
    create_segment(sim, (-2, 60), (-2, -60), category='tram', material='concrete', name='Down Tram') # 1

    # up road
    create_quadratic_bezier_curve(sim, (60, 55), (6, 60), (6, 40), category='general', name='Up Bottom') # 2
    create_segment(sim, (6, 40), (6, -40), category='general', material='asphalt', name='Up Road') # 3
    create_quadratic_bezier_curve(sim, (6, -40), (6, -60), (60, -55), category='general', name='Up Top') # 4
    
    # down road
    create_quadratic_bezier_curve(sim, (-60, -55), (-6, -55), (-6, -40), category='general', name='Down Top') # 5 
    create_segment(sim, (-6, -40), (-6, 40), category='general', material='asphalt', name='Down Road') # 6
    create_quadratic_bezier_curve(sim, (-6,40), (-6, 55), (-60, 55), category='general', name='Down Bottom') # 7

