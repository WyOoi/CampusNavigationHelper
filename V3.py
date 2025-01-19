import json
import random
import os
import tkinter as tk
from tkinter import messagebox
import turtle
import time
import gmplot
import webbrowser

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

        def display_home():
            for widget in content_frame.winfo_children():
                widget.destroy()
            tk.Label(content_frame, text="Welcome to Campus Navigation Helper", font=("Helvetica", 16)).pack(pady=20)

        def display_save_location():
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Save Location", font=("Helvetica", 14)).pack(pady=10)
            tk.Label(content_frame, text="Location Name:").pack()
            location_entry = tk.Entry(content_frame, width=30)
            location_entry.pack()

            tk.Label(content_frame, text="Description:").pack()
            description_entry = tk.Entry(content_frame, width=30)
            description_entry.pack()

            def save_location():
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

        def display_transport_updates():
            for widget in content_frame.winfo_children():
                widget.destroy()
    
            tk.Label(content_frame, text="Transport Updates", font=("Helvetica", 14)).pack(pady=10)

            # URL for transport updates (replace with your real URL)
            transport_url = "http://bustrackerutem.atwebpages.com/"  # Change this to your actual URL

            def open_transport_updates():
                webbrowser.open(transport_url)

            tk.Button(content_frame, text="View Transport Updates", command=open_transport_updates, width=20).pack(pady=10)


        def display_heatmap():
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Heatmap of Crowded Areas", font=("Helvetica", 14)).pack(pady=10)

            # Initialize gmplot (Google Map Plotter)
            gmap = gmplot.GoogleMapPlotter(2.310405, 102.314717, 13)  # Replace with your campus latitude and longitude

            # Randomly generate crowded area data (latitude, longitude)
            crowded_areas = [
                (2.310405, 102.314717),  # Sample coordinates, replace with real data
                (2.311048, 102.314438),
                (2.310281, 102.314223),
                # Add more locations here
            ]
            
            # Create the heatmap
            latitudes, longitudes = zip(*crowded_areas)
            gmap.heatmap(latitudes, longitudes)

            # Save the heatmap to an HTML file
            heatmap_file = "heatmap.html"
            gmap.draw(heatmap_file)

            # Open the heatmap in a web browser
            webbrowser.open(heatmap_file)

            tk.Label(content_frame, text="Heatmap generated. Opening in browser...", font=("Helvetica", 12)).pack(pady=10)

        def display_simulate_route():
            for widget in content_frame.winfo_children():
                widget.destroy()

            tk.Label(content_frame, text="Simulate Route", font=("Helvetica", 14)).pack(pady=10)
            tk.Label(content_frame, text="Starting Location:").pack()
            start_entry = tk.Entry(content_frame, width=30)
            start_entry.pack()

            tk.Label(content_frame, text="Destination:").pack()
            end_entry = tk.Entry(content_frame, width=30)
            end_entry.pack()

            def simulate_route():
                start = start_entry.get()
                end = end_entry.get()
                if start in self.locations and end in self.locations:
                    messagebox.showinfo("Route", f"Starting: {start}\nWeather: {self.weather_data}\nDestination: {end}")
                else:
                    messagebox.showerror("Error", "Invalid locations. Please ensure both locations are saved.")

            tk.Button(content_frame, text="Simulate", command=simulate_route).pack(pady=10)

        # Sidebar for navigation
        sidebar = tk.Frame(root, width=200, bg="gray")
        sidebar.pack(side="left", fill="y")

        tk.Button(sidebar, text="Home", command=display_home, width=20).pack(pady=10)
        tk.Button(sidebar, text="Save Location", command=display_save_location, width=20).pack(pady=10)
        tk.Button(sidebar, text="Transport Updates", command=display_transport_updates, width=20).pack(pady=10)
        tk.Button(sidebar, text="Heatmap", command=display_heatmap, width=20).pack(pady=10)
        tk.Button(sidebar, text="Simulate Route", command=display_simulate_route, width=20).pack(pady=10)
        tk.Button(sidebar, text="Exit", command=lambda: (self.save_data(), root.destroy()), width=20).pack(pady=10)

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

