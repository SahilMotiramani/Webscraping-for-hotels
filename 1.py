import tkinter as tk
from tkinter import ttk
import sqlite3

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Page")
        self.geometry("400x100")

        self.search_frame = tk.Frame(self, pady=20, bg="white")
        self.search_frame.pack(fill=tk.X, pady=0)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(self.search_frame, textvariable=self.search_var, width=20, font=("Cambria", 12), justify="center")
        self.search_entry.insert(0, "Enter city name")
        self.search_entry.bind("<KeyRelease>", self.update_city_list)  # Bind the KeyRelease event
        self.search_entry.pack(side=tk.LEFT, padx=20)

        self.listbox = tk.Listbox(self.search_frame, font=("Cambria", 12))
        self.listbox.pack(fill=tk.X, padx=20)
        self.listbox.bind("<<ListboxSelect>>", self.copy_selected_city)  # Bind the ListboxSelect event

        self.cities = []  # Store all city names
        self.load_cities()  # Load all cities initially

    def load_cities(self):
        # Connect to the database
        conn = sqlite3.connect('hotels.db')
        cursor = conn.cursor()
        
        # Fetch city names from the 'city' table
        cursor.execute("SELECT name FROM city")
        self.cities = [row[0] for row in cursor.fetchall()]
        
        self.update_listbox()  # Update the listbox
        
        conn.close()

    def update_city_list(self, event):
        # Filter cities based on search input
        search_input = self.search_var.get().strip().lower()
        filtered_cities = [city for city in self.cities if city.lower().startswith(search_input)]
        
        self.update_listbox(filtered_cities)  # Update the listbox

    def update_listbox(self, cities=None):
        self.listbox.delete(0, tk.END)  # Clear the listbox
        if cities:
            for city in cities:
                self.listbox.insert(tk.END, city)
        else:
            for city in self.cities:
                self.listbox.insert(tk.END, city)

    def copy_selected_city(self, event):
        # Get the selected city from the listbox
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_city = self.listbox.get(selected_index)
            # Copy the selected city to the search box
            self.search_var.set(selected_city)

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
