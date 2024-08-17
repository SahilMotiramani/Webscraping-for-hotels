import tkinter as tk
from PIL import Image, ImageTk

class HomePage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Home Page")
        self.geometry("800x600")
        
        # Search Box Section
        self.search_frame = tk.Frame(self, pady=20, bg="#BBE2EC")
        self.search_frame.pack(fill=tk.X, pady=0)  # Add padding to move it towards the center

        self.search_entry = tk.Entry(self.search_frame, width=20, font=("Cambria", 12), justify="center", bg="#EEEEEE")
        self.search_entry.insert(0, "Enter city name")  # Set placeholder text
        self.search_entry.bind("<FocusIn>", self.clear_placeholder)  # Bind FocusIn event to clear placeholder
        self.search_entry.bind("<FocusOut>", self.restore_placeholder)  # Bind FocusOut event to restore placeholder
        self.search_entry.pack(side=tk.LEFT, padx=(300, 20))  # Add right padding
        
        self.search_button = tk.Button(self.search_frame, text="Search", bg="#9B4444", fg="white", font=("Cambria", 12), command=self.search)
        self.search_button.pack(side=tk.LEFT)
        
        # Offers Section
        self.offers_frame = tk.Frame(self, bg="#BBE2EC", pady=0)
        self.offers_frame.pack(fill=tk.BOTH, expand=True)
        
        self.offers_label = tk.Label(self.offers_frame, text="Offers", font=("Cambria", 25, "bold"), bg="#BBE2EC")
        self.offers_label.pack()

        # Load and display the image
        offer_image = Image.open("offer.png")  # Assuming "offer.png" is in the current directory
        offer_image = offer_image.resize((800, 200), Image.LANCZOS)  # Resize the image to match the width of the window
        offer_image = ImageTk.PhotoImage(offer_image)
        self.offer_image_label = tk.Label(self.offers_frame, image=offer_image, bg="white")
        self.offer_image_label.image = offer_image  # Retain reference to the image to prevent garbage collection
        self.offer_image_label.pack(fill=tk.X)  # Fill the width of the frame

        # Explore India Section
        self.explore_frame = tk.Frame(self, bg="#BBE2EC", pady=0)
        self.explore_frame.pack(fill=tk.BOTH, expand=True)
        
        self.explore_label = tk.Label(self.explore_frame, text="Incredible India", font=("Cambria", 22, "bold"), bg="#BBE2EC")
        self.explore_label.pack()  # Align the text to the left (west) side

        
        self.cities = ["Mumbai", "Delhi", "Kolkata", "Jaipur", "Bangalore", "Lonavala"]
        for city in self.cities:
            # Create frame for each pair of image and button
            pair_frame = tk.Frame(self.explore_frame, bg="#BBE2EC")
            pair_frame.pack(side=tk.LEFT, padx=12, pady=10)  # Adjust padding as needed
            
            # Load image and resize
            img = Image.open(f"{city.lower()}.png")  # Assuming images are named after cities in lowercase
            img = img.resize((100, 100), Image.LANCZOS)  # Resize image to fit within a 80x80 box
            
            # Convert image to Tkinter PhotoImage
            img = ImageTk.PhotoImage(img)
            
            # Create label to display image
            img_label = tk.Label(pair_frame, image=img, bg="#9B4444")
            img_label.image = img  # Retain reference to the image to prevent garbage collection
            img_label.pack()
            
            # Create button for city
            button = tk.Button(pair_frame, text=city, bg="#9B4444", fg="white", font=("Cambria", 12), command=lambda c=city: self.explore_city(c))
            button.pack(pady=5)
        
    def search(self):
        city = self.search_entry.get()
        print("Searching for:", city)  # You can replace this with actual search functionality
    
    def explore_city(self, city):
        print("Exploring:", city)  # You can replace this with actual functionality
        
    def clear_placeholder(self, event):
        if self.search_entry.get() == "Enter city name":
            self.search_entry.delete(0, tk.END)

    def restore_placeholder(self, event):
        if not self.search_entry.get():
            self.search_entry.insert(0, "Enter city name")

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()