import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Page")
        self.geometry("800x600")

        self.search_frame = tk.Frame(self, pady=20, bg="white")
        self.search_frame.pack(fill=tk.X, pady=0)

        self.search_entry = tk.Entry(self.search_frame, width=20, font=("Cambria", 12), justify="center", bg="#EEEEEE")
        self.search_entry.insert(0, "Enter city name")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.pack(side=tk.LEFT, padx=(300, 20))
        
        self.search_button = tk.Button(self.search_frame, text="Search", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.search)
        self.search_button.pack(side=tk.LEFT)
        
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
            
            button = tk.Button(pair_frame, text=city, bg="#9B4444", fg="white", font=("Cambria", 12 , "bold"), command=lambda c=city: self.explore_city(c))
            button.pack(pady=5)
        
    def search(self):
        city = self.search_entry.get().strip()

        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        file_data = retrieve_csv_from_database(city)
        if file_data:
            # Display the data in a new window
            root = tk.Tk()
            root.title("Hotels")
            root.geometry("800x600")  # Set the window size to 800x600

            # Create a treeview widget
            tree = ttk.Treeview(root, style="Custom.Treeview")

            # Configure columns
            columns = ["ID", "Name", "Price", "Rating", "Description", "Link"]
            column_widths = {"ID": 40, "Name": 200, "Price": 50, "Rating": 60, "Description": 300, "Link": 200}
            tree["columns"] = columns
            tree["show"] = "headings"
            
            # Add columns to the treeview with specified widths
            for col in columns:
                tree.column(col, width=column_widths.get(col, 100))
                tree.heading(col, text=col)

            # Insert data rows with alternating row colors
            for i, row in enumerate(file_data):
                description_lines = self.split_text_into_lines(row[4], 60)  # Adjust the width as needed
                name_lines = self.split_text_into_lines(row[1], 30)  # Adjust the width as needed
                max_lines = max(len(name_lines), len(description_lines))
                for j in range(max_lines):
                    # Handle empty values for rows after the first row
                    name = name_lines[j] if j < len(name_lines) else ""
                    description = description_lines[j] if j < len(description_lines) else ""
                    if j == 0:
                        tree.insert("", tk.END, values=(row[0], name, row[2], row[3], description, row[5]))
                    else:
                        tree.insert("", tk.END, values=("", name, "", "", description, ""))
                    
                    # Apply tag to alternate rows for color formatting
                    if i % 2 == 0:
                        tree.tag_configure("even", background="lightgrey")
                        tree.item(tree.get_children()[-1], tags=("even",))
                    else:
                        tree.tag_configure("odd", background="white")
                        tree.item(tree.get_children()[-1], tags=("odd",))

            tree.pack(fill="both", expand=True)
            root.mainloop()
        else:
            messagebox.showerror("Error", f"No data found for {city}")
        
    def explore_city(self, city):
        print("Exploring:", city)
        
    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter city name":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter city name")

    def split_text_into_lines(self, text, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

def retrieve_csv_from_database(city):
    conn = sqlite3.connect('hotels.db')
    cursor = conn.cursor()
    try:
        cursor.execute(f'SELECT * FROM "{city}"')
        file_data = cursor.fetchall()  # Fetch all rows
        conn.close()
        return file_data
    except sqlite3.OperationalError:
        conn.close()
        return None

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()