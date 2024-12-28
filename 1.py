import time
from datetime import datetime
import random
import math

# Feature 1: Save Frequently Visited Locations
class LocationManager:
    def __init__(self):
        self.locations = {}

    def save_location(self, name, coordinates):
        if not isinstance(coordinates, tuple) or len(coordinates) != 2:
            print("Invalid coordinates. Please provide a tuple with two numeric values.")
            return
        self.locations[name] = coordinates
        print(f"Location '{name}' saved successfully!")

    def show_saved_locations(self):
        if not self.locations:
            print("\nNo saved locations found.")
            return
        print("\nSaved Locations:")
        for name, coords in self.locations.items():
            print(f"- {name}: {coords}")

# Feature 2: Fetch Real-Time Bus Updates (Simulated)
def get_real_time_bus_updates(buses=None):
    if buses is None:
        buses = ["Bus A", "Bus B", "Bus C"]
    updates = {
        bus: f"Arriving in {random.randint(1, 15)} minutes"
        for bus in buses
    }
    return updates

# Feature 3: Visualize Walking Paths or Heatmaps of Crowded Areas (Simulated)
def generate_heatmap():
    print("\nHeatmap of crowded areas (simulated):")
    areas = ["Library", "Cafeteria", "Main Gate", "Sports Complex"]
    for area in areas:
        crowd_density = random.randint(1, 100)
        print(f"- {area}: {crowd_density}% crowded")

# Feature 4: Simulate Optimal Routes Based on Time and Weather (Simplified)
def calculate_distance(coord1, coord2):
    # Using Euclidean distance for simplicity
    if not (isinstance(coord1, tuple) and isinstance(coord2, tuple)):
        raise ValueError("Coordinates must be tuples with two numeric values.")
    return math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)

def simulate_optimal_route(current_location, destination, weather):
    try:
        distance = calculate_distance(current_location, destination)
    except ValueError as e:
        print(e)
        return
    time_estimate = distance / 5  # Assuming an average walking speed of 5 units/hour

    if weather == "Rainy":
        time_estimate *= 1.5  # Slower walking in rain

    print("\nOptimal Route Simulation:")
    print(f"Distance: {distance:.2f} units")
    print(f"Estimated Time: {time_estimate:.2f} hours ({'Rainy' if weather == 'Rainy' else 'Clear'} weather)")

# Main Program
def main():
    location_manager = LocationManager()

    predefined_inputs = ["1", "Library", "10", "20", "2", "3", "4", "5", "10", "20", "30", "40", "Clear", "6"]
    input_counter = 0

    def mock_input(prompt):
        nonlocal input_counter
        value = predefined_inputs[input_counter]
        input_counter += 1
        print(f"{prompt}{value}")
        return value

    while True:
        print("\nCampus Navigation Helper")
        print("1. Save a frequently visited location")
        print("2. Show saved locations")
        print("3. Get real-time bus updates")
        print("4. Visualize walking paths or crowded heatmaps")
        print("5. Simulate an optimal route")
        print("6. Exit")

        choice = mock_input("Choose an option: ")

        if choice == "1":
            name = mock_input("Enter location name: ")
            try:
                x = float(mock_input("Enter X coordinate: "))
                y = float(mock_input("Enter Y coordinate: "))
                location_manager.save_location(name, (x, y))
            except ValueError:
                print("Invalid input. Coordinates must be numeric values.")

        elif choice == "2":
            location_manager.show_saved_locations()

        elif choice == "3":
            buses = mock_input("Enter bus names separated by commas (leave blank for default): ").split(',')
            if buses == ['']:
                buses = None
            updates = get_real_time_bus_updates(buses)
            print("\nReal-Time Bus Updates:")
            for bus, update in updates.items():
                print(f"- {bus}: {update}")

        elif choice == "4":
            generate_heatmap()

        elif choice == "5":
            try:
                x1 = float(mock_input("Enter current location X coordinate: "))
                y1 = float(mock_input("Enter current location Y coordinate: "))
                x2 = float(mock_input("Enter destination X coordinate: "))
                y2 = float(mock_input("Enter destination Y coordinate: "))
                weather = mock_input("Enter weather condition (Clear/Rainy): ")
                simulate_optimal_route((x1, y1), (x2, y2), weather)
            except ValueError:
                print("Invalid input. Coordinates must be numeric values.")

        elif choice == "6":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

        time.sleep(1)

if __name__ == "__main__":
    main()
