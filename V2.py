import json
import random
import os
import tkinter as tk
from tkinter import messagebox

class CampusNavigationHelper:
    def __init__(self):
        self.locations = {}
        self.transport_updates = []
        self.crowded_areas = []
        self.weather_data = "Clear"
        self.load_data()

    def save_data(self):
        with open("campus_data.json", "w") as file:
            json.dump({"locations": self.locations, "transport_updates": self.transport_updates, "crowded_areas": self.crowded_areas}, file)

    def load_data(self):
        if os.path.exists("campus_data.json"):
            with open("campus_data.json", "r") as file:
                data = json.load(file)
                self.locations = data.get("locations", {})
                self.transport_updates = data.get("transport_updates", [])
                self.crowded_areas = data.get("crowded_areas", [])

    def display_menu(self):
        root = tk.Tk()
        root.title("Campus Navigation Helper")

        def save_location():
            def save():
                location_name = location_entry.get()
                description = description_entry.get()
                if location_name and description:
                    self.locations[location_name] = description
                    messagebox.showinfo("Success", f"Location '{location_name}' saved successfully.")
                    save_window.destroy()
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

            save_window = tk.Toplevel(root)
            save_window.title("Save Location")

            tk.Label(save_window, text="Location Name:").pack()
            location_entry = tk.Entry(save_window)
            location_entry.pack()

            tk.Label(save_window, text="Description:").pack()
            description_entry = tk.Entry(save_window)
            description_entry.pack()

            tk.Button(save_window, text="Save", command=save).pack()

        def fetch_transport_updates():
            self.transport_updates = [
                "Bus A: Arriving in 5 minutes",
                "Bus B: Delayed by 10 minutes",
                "Bus C: Operating on schedule"
            ]
            updates = "\n".join(self.transport_updates)
            messagebox.showinfo("Transport Updates", updates)

        def visualize_heatmap():
            heatmap_window = tk.Toplevel(root)
            heatmap_window.title("Heatmap of Crowded Areas")

            canvas = tk.Canvas(heatmap_window, width=400, height=400, bg="lightblue")
            canvas.pack()

            for _ in range(random.randint(5, 15)):
                x = random.randint(10, 390)
                y = random.randint(10, 390)
                intensity = random.randint(1, 10)
                color = "red" if intensity > 5 else "yellow"
                canvas.create_oval(x-5, y-5, x+5, y+5, fill=color)

        def simulate_route():
            def show_route():
                start = start_entry.get()
                end = end_entry.get()
                if start in self.locations and end in self.locations:
                    messagebox.showinfo("Route", f"Starting: {start}\nWeather: {self.weather_data}\nDestination: {end}")
                    route_window.destroy()
                else:
                    messagebox.showerror("Error", "Invalid locations. Please ensure both locations are saved.")

            route_window = tk.Toplevel(root)
            route_window.title("Simulate Route")

            tk.Label(route_window, text="Starting Location:").pack()
            start_entry = tk.Entry(route_window)
            start_entry.pack()

            tk.Label(route_window, text="Destination:").pack()
            end_entry = tk.Entry(route_window)
            end_entry.pack()

            tk.Button(route_window, text="Simulate", command=show_route).pack()

        tk.Button(root, text="Save Location", command=save_location).pack(pady=10)
        tk.Button(root, text="Fetch Transport Updates", command=fetch_transport_updates).pack(pady=10)
        tk.Button(root, text="Visualize Heatmap", command=visualize_heatmap).pack(pady=10)
        tk.Button(root, text="Simulate Route", command=simulate_route).pack(pady=10)
        tk.Button(root, text="Exit", command=lambda: (self.save_data(), root.destroy())).pack(pady=10)

        root.mainloop()

# Entry point for the program
def main():
    app = CampusNavigationHelper()
    app.display_menu()

if __name__ == "__main__":
    main()
