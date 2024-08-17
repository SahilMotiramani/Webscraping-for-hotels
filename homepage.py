import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class SearchPage(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Search Hotels")
        self.geometry("800x600")

        self.search_label = tk.Label(self, text="Enter City Name:", font=("Cambria", 12))
        self.search_label.pack(pady=10)

        self.search_entry = tk.Entry(self, width=20, font=("Cambria", 12))
        self.search_entry.pack(pady=5)

        self.search_button = tk.Button(self, text="Search", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.search)
        self.search_button.pack(pady=10)

        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(pady=10)

        self.filter_label = tk.Label(self.filter_frame, text="Filter by:", font=("Cambria", 12))
        self.filter_label.grid(row=0, column=0, padx=(0, 10))

        self.filter_var = tk.StringVar(self)
        self.filter_var.set("Price High to Low")
        self.filter_options = ["Price High to Low", "Price Low to High", "Ratings High to Low"]
        self.filter_dropdown = ttk.OptionMenu(self.filter_frame, self.filter_var, *self.filter_options)
        self.filter_dropdown.grid(row=0, column=1)

        self.filter_button = tk.Button(self.filter_frame, text="Filter", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.filter_hotels)
        self.filter_button.grid(row=0, column=2, padx=(10, 0))

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def search(self):
        city = self.search_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return
        
        # Retrieve hotel information from the database
        hotel_data = retrieve_hotel_data(city)
        if hotel_data:
            # Clear existing treeview data
            self.tree.delete(*self.tree.get_children())

            # Insert hotel data into treeview
            for row in hotel_data:
                self.tree.insert("", tk.END, values=row)
        else:
            messagebox.showerror("Error", f"No hotel data found for {city}")

    def filter_hotels(self):
        selected_filter = self.filter_var.get()
        # Implement filtering logic here
        print("Filtering hotels by:", selected_filter)

def retrieve_hotel_data(city):
    conn = sqlite3.connect('hotels.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM "{city}"')
        hotel_data = cursor.fetchall()
        conn.close()
        return hotel_data
    except sqlite3.OperationalError:
        conn.close()
        return None

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Page")
        self.geometry("800x600")

        self.offers_frame = tk.Frame(self, bg="white", pady=0)
        self.offers_frame.pack(fill=tk.BOTH, expand=True)

        self.offers_label = tk.Label(self.offers_frame, text="Offers", font=("Cambria", 25, "bold"), bg="white")
        self.offers_label.pack()

        offer_image = Image.open("offer.png")
        offer_image = offer_image.resize((800, 200), Image.LANCZOS)
        offer_image = ImageTk.PhotoImage(offer_image)
        self.offer_image_label = tk.Label(self.offers_frame, image=offer_image, bg="white")
        self.offer_image_label.image = offer_image
        self.offer_image_label.pack(fill=tk.X)

        self.explore_frame = tk.Frame(self, bg="white", pady=0)
        self.explore_frame.pack(fill=tk.BOTH, expand=True)

        self.explore_label = tk.Label(self.explore_frame, text="Incredible India", font=("Cambria", 22, "bold"), bg="white")
        self.explore_label.pack()

        search_button = tk.Button(self.explore_frame, text="Search for City", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.open_search_page)
        search_button.pack(pady=10)

        self.cities = ["Mumbai", "Delhi", "Kolkata", "Jaipur", "Bangalore", "Lonavala"]
        for city in self.cities:
            pair_frame = tk.Frame(self.explore_frame, bg="white")
            pair_frame.pack(side=tk.LEFT, padx=12, pady=10)

            img = Image.open(f"{city.lower()}.png")
            img = img.resize((100, 100), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(pair_frame, image=img, bg="Lightgrey")
            img_label.image = img
            img_label.pack()

            button = tk.Button(pair_frame, text=city, bg="#9B4444", fg="white", font=("Cambria", 12, "bold"), command=lambda c=city: self.explore_city(c))
            button.pack(pady=5)

    def explore_city(self, city):
        print("Exploring:", city)

    def open_search_page(self):
        search_page = SearchPage(self)

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
