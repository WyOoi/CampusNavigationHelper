import json
import os
import tkinter as tk
from tkinter import messagebox
import turtle
import time
import gmplot
import webbrowser
import googlemaps

API_KEY = "AIzaSyDHG4BxBfhyhGdVAcwIoABp4F-lG272Kjo"  # Replace with your actual Google Maps API key
gmaps = googlemaps.Client(key=API_KEY)

def geocode(location_name):
        try:
            geocode_result = gmaps.geocode(location_name)
            if geocode_result:
                location = geocode_result[0]['geometry']['location']
                return location['lat'], location['lng']
            else:
                return None
        except Exception as e:
            print(f"Error geocoding location '{location_name}': {e}")
            return None

def draw_opening_animation():
    screen = turtle.Screen()
    screen.title("Campus Navigation Helper")
    screen.bgcolor("white")
    screen.setup(width=600, height=600)

    pen = turtle.Turtle()
    pen.speed(3)
    pen.hideturtle()

    # Draw a compass-like circle
    pen.penup()
    pen.goto(0, -150)
    pen.pendown()
    pen.pensize(3)
    pen.color("blue")
    pen.circle(150)

    # Draw directional lines
    directions = ["N", "E", "S", "W"]
    angle = 90
    pen.color("black")
    for direction in directions:
        pen.penup()
        pen.goto(0, 0)
        pen.setheading(angle)
        pen.forward(150)
        pen.write(direction, align="center", font=("Arial", 16, "bold"))
        pen.backward(150)
        angle -= 90

    # Draw a navigation arrow
    pen.penup()
    pen.goto(0, -20)
    pen.setheading(60)
    pen.pendown()
    pen.color("red")
    pen.begin_fill()
    for _ in range(3):
        pen.forward(40)
        pen.left(120)
    pen.end_fill()

    # Display welcome message
    pen.penup()
    pen.goto(0, -200)
    pen.color("green")
    pen.write("Welcome to Campus Navigation Helper!", align="center", font=("Arial", 18, "bold"))

    # Pause for 3 seconds before closing animation
    time.sleep(3)
    screen.bye()

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
        root.geometry("600x400")

        def display_home(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()
            tk.Label(content_frame, text="Welcome to Campus Navigation Helper", font=("Helvetica", 16)).pack(pady=20)

        def display_save_location(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Save Location", font=("Helvetica", 14)).pack(pady=10)
            tk.Label(content_frame, text="Location Name:").pack()
            location_entry = tk.Entry(content_frame, width=30)
            location_entry.pack()

            tk.Label(content_frame, text="Description:").pack()
            description_entry = tk.Entry(content_frame, width=30)
            description_entry.pack()

            def save_location(*args, **kwargs):
                location_name = location_entry.get()
                description = description_entry.get()
                if location_name and description:
                    self.locations[location_name] = description
                    messagebox.showinfo("Success", f"Location '{location_name}' saved successfully.")
                    location_entry.delete(0, tk.END)
                    description_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

            tk.Button(content_frame, text="Save", command=save_location).pack(pady=10)

        def display_transport_updates(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Transport Updates", font=("Helvetica", 14)).pack(pady=10)

            # URL for transport updates (replace with your real URL)
            transport_url = kwargs.get('transport_url', "http://bustrackerutem.atwebpages.com/")  # Default URL

            def open_transport_updates():
                webbrowser.open(transport_url)

            tk.Button(content_frame, text="View Transport Updates", command=open_transport_updates, width=20).pack(pady=10)

        def display_heatmap(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Heatmap of Crowded Areas", font=("Helvetica", 14)).pack(pady=10)

            # Initialize gmplot (Google Map Plotter)
            gmap = gmplot.GoogleMapPlotter(2.310405, 102.314717, 13)  # Replace with your campus latitude and longitude

            # Fetch crowded areas from kwargs (defaults if not provided)
            crowded_areas = kwargs.get('crowded_areas', [
                (2.310405, 102.314717),  # Sample coordinates, replace with real data
                (2.311048, 102.314438),
                (2.310281, 102.314223),
            ])
            
            # Create the heatmap
            latitudes, longitudes = zip(*crowded_areas)
            gmap.heatmap(latitudes, longitudes)

            # Save the heatmap to an HTML file
            heatmap_file = "heatmap.html"
            gmap.draw(heatmap_file)

            # Open the heatmap in a web browser
            webbrowser.open(heatmap_file)

            tk.Label(content_frame, text="Heatmap generated. Opening in browser...", font=("Helvetica", 12)).pack(pady=10)

        def display_simulate_route(*args, **kwargs):
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Simulate Route", font=("Helvetica", 14)).pack(pady=10)

            tk.Label(content_frame, text="Starting Location:").pack()
            start_var = tk.StringVar(content_frame)
            start_menu = tk.OptionMenu(content_frame, start_var, *self.locations.keys())
            start_menu.pack()

            tk.Label(content_frame, text="Destination:").pack()
            end_var = tk.StringVar(content_frame)
            end_menu = tk.OptionMenu(content_frame, end_var, *self.locations.keys())
            end_menu.pack()
            
            if not self.locations:
                tk.Label(content_frame, text="No locations saved. Please save locations first!", fg="red").pack(pady=10)
                return
            
            def plot_on_google_maps():
                start = start_var.get()
                end = end_var.get()

                if start and end:
                # Get coordinates for the start and end locations
                    start_coords = geocode(start)
                    end_coords = geocode(end)
                        
                    if start_coords and end_coords:
                # Generate a Google Maps URL
                        google_maps_url = (
                            f"https://www.google.com/maps/dir/?api=1"
                            f"&origin={start_coords[0]},{start_coords[1]}"
                            f"&destination={end_coords[0]},{end_coords[1]}"
                            f"&travelmode=walking"  # You can change to driving, bicycling, or transit
                        )

                # Open the Google Maps route in the default browser
                        webbrowser.open(google_maps_url)
                        tk.Label(content_frame, text="Route opened in Google Maps!", fg="green").pack(pady=10)
                    else:
                        messagebox.showerror("Error", "Selected locations are not saved. Please ensure both locations exist.")
                else:
                    messagebox.showerror("Error", "Please select both a starting location and a destination.")

            tk.Button(content_frame, text="Plot Route on Google Maps", command=plot_on_google_maps).pack(pady=20)

    # Additional interactivity: Show a summary of the route
            summary_frame = tk.Frame(content_frame, bg="lightgray", bd=2, relief="sunken")
            summary_frame.pack(pady=10, fill="x", padx=20)

            tk.Label(summary_frame, text="Route Summary", bg="lightgray", font=("Helvetica", 12, "bold")).pack(pady=5)
            summary_text = tk.Text(summary_frame, height=4, wrap="word", state="disabled")
            summary_text.pack(pady=5, padx=10, fill="x")

            def update_summary(*args):
                start = start_var.get()
                end = end_var.get()

                summary_text.config(state="normal")
                summary_text.delete(1.0, tk.END)
                if start and end:
                    summary_text.insert(
                        tk.END,
                        f"Starting Location: {start}\n"
                        f"Destination: {end}\n"
                        f"Route Type: Walking\n"
                    )
                else:
                    summary_text.insert(tk.END, "Select both a starting location and a destination to view the summary.")
                summary_text.config(state="disabled")

            start_var.trace("w", update_summary)
            end_var.trace("w", update_summary)


        # Sidebar for navigation
        sidebar = tk.Frame(root, width=200, bg="gray")
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="Home", command=lambda: display_home(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Save Location", command=lambda: display_save_location(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Transport Updates", command=lambda: display_transport_updates(transport_url="http://bustrackerutem.atwebpages.com/"), width=20).pack(pady=10)
        tk.Button(sidebar, text="Heatmap", command=lambda: display_heatmap(crowded_areas=[
            (2.310405, 102.314717), (2.311048, 102.314438), (2.310281, 102.314223)
        ]), width=20).pack(pady=10)
        tk.Button(sidebar, text="Simulate Route", command=lambda: display_simulate_route(), width=20).pack(pady=10)
        tk.Button(sidebar, text="Exit", command=lambda: (self.save_data(), root.quit()), width=20).pack(pady=10)

        # Main content frame
        content_frame = tk.Frame(root, bg="white")
        content_frame.pack(side="right", fill="both", expand=True)

        display_home()  # Display the home page initially

        root.mainloop()

def main():
    draw_opening_animation()
    app = CampusNavigationHelper()
    app.display_menu()

if __name__ == "__main__":
    main()

