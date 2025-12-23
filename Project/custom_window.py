import trafficSimulator as ts
import dearpygui.dearpygui as dpg

from event_manager import EventManager

class CustomWindow(ts.Window):
    def __init__(self, simulation):
        super().__init__(simulation)
        self.event_manager = EventManager(simulation)

    def draw_bg(self):
        # Set background to Blue
        super().draw_bg(color=(100, 149, 237))

    def draw_segments(self):
        # Draw Scenery (Land)
        # Top Land (Y > 40)
        dpg.draw_rectangle((-2000, 40), (2000, 2000), color=(60, 179, 113), fill=(60, 179, 113), parent="Canvas") # Medium Sea Green
        # Bottom Land (Y < -40)
        dpg.draw_rectangle((-2000, -2000), (2000, -40), color=(60, 179, 113), fill=(60, 179, 113), parent="Canvas")

        for segment in self.simulation.segments:
            # Determine color and thickness based on category and material
            # Default values
            color = (180, 180, 220) 
            thickness = 3.5 * self.zoom
            
            # Retrieve attributes if they exist (added via helper functions)
            material = getattr(segment, 'material', 'asphalt')
            category = getattr(segment, 'category', 'general')

            # Material Colors (Base)
            if material == 'asphalt':
                color = (20, 20, 20) #black
            elif material == 'concrete':
                color = (180, 180, 180) #gray
            elif material == 'gravel':
                color = (150, 50, 20) #light brown
            elif material == 'dirt':
                color = (100, 50, 50) #dark brown
            
            # Category Overrides/Adjustments
            if category == 'tram':
                color = (255, 215, 0) # Gold for tram line
                thickness = 5.0 * self.zoom
            elif category == 'highway':
                thickness = 5.0 * self.zoom
            
            dpg.draw_polyline(segment.points, color=color, thickness=thickness, parent="Canvas")

    def draw_vehicles(self):
        super().draw_vehicles()
        # Draw events with special colors
        for segment in self.simulation.segments:
            for vehicle_id in segment.vehicles:
                vehicle = self.simulation.vehicles[vehicle_id]
                if hasattr(vehicle, 'event_type'):
                    # Determine color based on event type
                    if vehicle.event_type == 'accident':
                        color = (255, 0, 0) # Red
                    elif vehicle.event_type == 'construction':
                        color = (255, 140, 0) # Orange
                    elif vehicle.event_type == 'animal':
                        color = (0, 255, 0) # Green
                    else:
                        color = (255, 255, 0)

                    progress = vehicle.x / segment.get_length()
                    position = segment.get_point(progress)
                    heading = segment.get_heading(progress)

                    node = dpg.add_draw_node(parent="Canvas")
                    # Draw a box or circle for event
                    dpg.draw_circle((0,0), 5, color=color, fill=color, parent=node)

                    translate = dpg.create_translation_matrix(position)
                    rotate = dpg.create_rotation_matrix(heading, [0, 0, 1])
                    dpg.apply_transform(node, translate*rotate)

    def render_loop(self):
        # Update Event Manager
        if hasattr(self, 'event_manager') and self.is_running:
            self.event_manager.update(self.simulation.dt)
            
        super().render_loop()

    def create_windows(self):
        super().create_windows()
        
        # Add Vehicle Info header to ControlsWindow
        with dpg.collapsing_header(label="Vehicle Info", parent="ControlsWindow", default_open=True):
            with dpg.table(tag="VehicleTable", header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True):
                dpg.add_table_column(label="Engine")
                dpg.add_table_column(label="AC Temp")
                dpg.add_table_column(label="DRL")
                dpg.add_table_column(label="Wipers")

    def update_panels(self):
        super().update_panels()
        
        # Update Vehicle Table
        if dpg.does_item_exist("VehicleTable"):
            # Clear existing rows (children of the table)
            dpg.delete_item("VehicleTable", children_only=True)
            
            # Re-add columns (clearing children removes columns too if they are children)
            dpg.add_table_column(label="Engine", parent="VehicleTable")
            dpg.add_table_column(label="AC Temp", parent="VehicleTable")
            dpg.add_table_column(label="DRL", parent="VehicleTable")
            dpg.add_table_column(label="Wipers", parent="VehicleTable")

            for vehicle in self.simulation.vehicles.values():
                with dpg.table_row(parent="VehicleTable"):
                    dpg.add_text(vehicle.engine_type)
                    dpg.add_text(f"{vehicle.ac_temperature:.1f}")
                    dpg.add_text(str(vehicle.DaytimeRunningLights))
                    dpg.add_text(str(vehicle.windshield_wipers))
