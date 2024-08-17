import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from PIL import Image, ImageTk
import webbrowser

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Page")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        window_width = 800
        window_height = 600

        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        self.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        self.create_search_section()
        self.create_offers_section()
        self.create_explore_section()

    def create_search_section(self):
        self.search_frame = tk.Frame(self, pady=20, bg="white")
        self.search_frame.pack(fill=tk.X, pady=0)

        self.search_var = tk.StringVar()
        self.search_var.set("Enter city name")
        self.search_entry = ttk.Combobox(self.search_frame, textvariable=self.search_var, width=20, font=("Cambria", 12), justify="center")
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)
        self.search_entry.bind("<KeyRelease>", self.update_city_list)
        self.search_entry.pack(side=tk.LEFT, padx=(300, 20))

        self.search_button = tk.Button(self.search_frame, text="Search", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.search)
        self.search_button.pack(side=tk.LEFT)

    def create_offers_section(self):
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

    def create_explore_section(self):
        self.explore_frame = tk.Frame(self, bg="white", pady=0)
        self.explore_frame.pack(fill=tk.BOTH, expand=True)

        self.explore_label = tk.Label(self.explore_frame, text="Incredible India", font=("Cambria", 22, "bold"), bg="white")
        self.explore_label.pack()

        canvas = tk.Canvas(self.explore_frame, bg="white", highlightthickness=0)
        canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        scrollbar = ttk.Scrollbar(self.explore_frame, orient="horizontal", command=canvas.xview)
        scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        canvas.configure(xscrollcommand=scrollbar.set)

        inner_frame = tk.Frame(canvas, bg="white")
        canvas.create_window((0,0), window=inner_frame, anchor="nw")

        self.cities = ["Mumbai", "Jaipur", "Bangalore", "Jammu", "Darjeeling","Ayodhya","Mahabaleshwar","Amritsar", "Kolkata","Lonavala"]
        for city in self.cities:
            pair_frame = tk.Frame(inner_frame, bg="white")
            pair_frame.pack(side=tk.LEFT, padx=5, pady=10)

            img = Image.open(f"{city.lower()}.png")
            img = img.resize((150, 150), Image.LANCZOS)
            img = ImageTk.PhotoImage(img)

            img_label = tk.Label(pair_frame, image=img, bg="Lightgrey")
            img_label.image = img
            img_label.pack()

            button = tk.Button(pair_frame, text=city, bg="#9B4444", fg="white", font=("Cambria", 12, "bold"), command=lambda c=city: self.explore_city(c))
            button.pack(pady=5)

        def update_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", update_scroll_region)

        canvas.bind_all("<MouseWheel>", lambda event: canvas.xview_scroll(-1*(event.delta), "units"))



    def search(self):
        city = self.search_var.get().strip()

        if not city:
            messagebox.showerror("Error", "Please enter a city name.")
            return

        file_data = retrieve_csv_from_database(city)
        if file_data:
            self.withdraw()
            self.display_table(file_data)
        else:
            messagebox.showerror("Error", f"No data found for {city}")

    def display_table(self, file_data):
        self.file_data = file_data
        self.table_window = tk.Toplevel(self)
        self.table_window.title("Hotels")
        self.table_window.geometry(f"800x600+{self.winfo_x()}+{self.winfo_y()}")

        self.table_window.protocol("WM_DELETE_WINDOW", self.on_table_close)

        self.create_filter_section()

        self.create_treeview(file_data)

        self.back_button = tk.Button(self.table_window, text="Back to search", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.go_back)
        self.back_button.pack(side=tk.BOTTOM, pady=0)

    def on_table_close(self):
        self.deiconify() 
        self.table_window.destroy() 

    def create_filter_section(self):
        self.filter_frame = tk.Frame(self.table_window, bg="white")
        self.filter_frame.pack(fill=tk.X)

        self.filter_label = tk.Label(self.filter_frame, text="Filter by:", bg="#9B4444", font=("Cambria", 12), fg="white")
        self.filter_label.place(x=300, y=5)

        self.filter_var = tk.StringVar()
        self.filter_var.set("Select Filter")

        self.filter_dropdown = ttk.OptionMenu(self.filter_frame, self.filter_var, "Select Filter", "Price: High to Low", "Price: Low to High", "Rating: High to Low", command=self.apply_filters)
        self.filter_dropdown.grid(row=0, column=1, padx=375, pady=5)

    def create_treeview(self, file_data):
        self.tree_frame = tk.Frame(self.table_window)
        self.tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.tree_frame, style="Custom.Treeview")
        self.columns = ["ID", "Name", "Price", "Rating", "Description", "Link"]
        self.column_widths = {"ID": 30, "Name": 170, "Price": 50, "Rating": 30, "Description": 290, "Link": 50}
        self.tree["columns"] = self.columns
        self.tree["show"] = "headings"

        for col in self.columns:
            self.tree.column(col, width=self.column_widths.get(col, 100))
            self.tree.heading(col, text=col)

        for i, row in enumerate(file_data):
            self.description_lines = self.split_text_into_lines(row[4], 60)
            self.name_lines = self.split_text_into_lines(row[1], 30)
            self.max_lines = max(len(self.name_lines), len(self.description_lines))
            for j in range(self.max_lines):
                self.name = self.name_lines[j] if j < len(self.name_lines) else ""
                self.description = self.description_lines[j] if j < len(self.description_lines) else ""
                if j == 0:
                    self.tree.insert("", tk.END, values=(row[0], self.name, row[2], row[3], self.description, row[5]))
                else:
                    self.tree.insert("", tk.END, values=("", self.name, "", "", self.description, ""))

                if i % 2 == 0:
                    self.tree.tag_configure("even", background="lightgrey")
                    self.tree.item(self.tree.get_children()[-1], tags=("even",))
                else:
                    self.tree.tag_configure("odd", background="white")
                    self.tree.item(self.tree.get_children()[-1], tags=("odd",))

        self.tree.pack(side="left", fill="both", expand=True)

        yscrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        yscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=yscrollbar.set)
        yscrollbar.bind("<MouseWheel>", lambda event: "break")

        self.tree.bind("<<TreeviewSelect>>", self.open_link)

        self.tree_frame.update_idletasks()
        self.tree.config(height=self.tree_frame.winfo_height())

    def go_back(self):
        self.on_table_close()

    def apply_filters(self, option):
        if option == "Select Filter":
            return

        sorted_data = self.file_data.copy()

        if "Price" in option:
            if "High to Low" in option:
                sort_key = lambda x: float(x[2].replace('₹', '').replace(',', ''))
                reverse = True
                sorted_data.sort(key=sort_key, reverse=reverse)
            elif "Low to High" in option:
                sort_key = lambda x: float(x[2].replace('₹', '').replace(',', ''))
                reverse = False
                sorted_data.sort(key=sort_key, reverse=reverse)
        elif "Rating" in option:
            sort_key = lambda x: float(x[3])
            reverse = "Low" in option
            sorted_data.sort(key=sort_key, reverse=reverse)
        elif "Name" in option:
            sort_key = lambda x: x[1].lower()
            sorted_data.sort(key=sort_key)

        self.update_table(sorted_data)

    def update_table(self, data):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, row in enumerate(data):
            self.description_lines = self.split_text_into_lines(row[4], 60)
            self.name_lines = self.split_text_into_lines(row[1], 30)
            self.max_lines = max(len(self.name_lines), len(self.description_lines))
            for j in range(self.max_lines):
                self.name = self.name_lines[j] if j < len(self.name_lines) else ""
                self.description = self.description_lines[j] if j < len(self.description_lines) else ""
                if j == 0:
                    self.tree.insert("", tk.END, values=(row[0], self.name, row[2], row[3], self.description, row[5]))
                else:
                    self.tree.insert("", tk.END, values=("", self.name, "", "", self.description, ""))

                if i % 2 == 0:
                    self.tree.tag_configure("even", background="lightgrey")
                    self.tree.item(self.tree.get_children()[-1], tags=("even",))
                else:
                    self.tree.tag_configure("odd", background="white")
                    self.tree.item(self.tree.get_children()[-1], tags=("odd",))

    def open_link(self, event):
        item = self.tree.selection()
        if item:
            link = self.tree.item(item, "values")[-1]
            if link:
                webbrowser.open_new_tab(link)

    def explore_city(self, city):
        file_data = retrieve_csv_from_database(city)
        if file_data:
            self.withdraw()
            self.display_table(file_data)
        else:
            messagebox.showerror("Error", f"No data found for {city}")

    def clear_placeholder(self, event):
        if self.search_var.get() == "Enter city name":
            self.search_var.set("")

    def restore_placeholder(self, event):
        if not self.search_var.get():
            self.search_var.set("Enter city name")

    def update_city_list(self, event):
        typed = self.search_var.get().lower()
        matched_cities = [city for city in self.cities if typed in city.lower()]
        self.search_entry['values'] = matched_cities

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
        file_data = cursor.fetchall()
        conn.close()
        return file_data
    except sqlite3.OperationalError:
        conn.close()
        return None

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()
