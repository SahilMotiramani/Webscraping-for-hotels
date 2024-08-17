import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
import urllib.parse

def scrape_hotels():
    global hotels  
    
    # Clear existing data from the treeview
    for widget in treeview_frame.winfo_children():
        widget.destroy()
    
    location = location_entry.get()
    search_query = urllib.parse.quote_plus(f"{location} hotels")
    url = f"https://www.google.com/travel/search?q={search_query}&qs=OAA&ved=0CAAQ5JsGahcKEwjgkdva_iO6EAxUAAAAAHQAAAAAQCw"
    
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    hotels = []  
    hotel_elements = soup.find_all("div", class_="pb2I5 SV2nb FMaDxf")

    for hotel in hotel_elements:
        name_element = hotel.find("h2", class_="BgYkof ogfYpf ykx2he")
        price_element = hotel.find("span", jsaction="mouseenter:JttVIc;mouseleave:VqIRre;")
        review_element = hotel.find("span", class_="KFi5wf lA0BZ")
        description_element = hotel.find("span", class_="lXJaOd")
        image_element = hotel.find("img")
        
        if name_element:
            name = name_element.text.strip()

            if price_element:
                price = price_element.text.strip()
            else:
                price = "Price information not available"

            if review_element:
                review = review_element.text.strip()
            else:
                review = "Rating information not available"

            if description_element:
                description = description_element.text.strip()
            else:
                description = "Description not available"

            # Extracting image URL from the src attribute
            image_url = image_element.get("src") if image_element else None

            hotels.append({
                'name': name,
                'price': price,
                'review': review,
                'description': description,
                'image_url': image_url
            })
    
    display_hotels(hotels)

def display_hotels(hotels):
    for index, hotel in enumerate(hotels):
        # Create a frame for each hotel
        hotel_frame = tk.Frame(treeview_frame)
        hotel_frame.pack(fill="x", pady=5)

        # Display hotel name
        name_label = tk.Label(hotel_frame, text=f"Name: {hotel['name']}")
        name_label.grid(row=0, column=0, sticky="w", padx=5)

        # Display hotel price
        price_label = tk.Label(hotel_frame, text=f"Price: {hotel['price']}")
        price_label.grid(row=0, column=1, sticky="w", padx=5)

        # Display hotel rating
        rating_label = tk.Label(hotel_frame, text=f"Rating: {hotel['review']}")
        rating_label.grid(row=0, column=2, sticky="w", padx=5)

        # Display hotel description
        description_label = tk.Label(hotel_frame, text=f"Description: {hotel['description']}")
        description_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=5)

        # Display hotel image if available
        if hotel['image_url']:
            response = requests.get(hotel['image_url'])
            if response.ok:
                img_data = response.content
                img = Image.open(BytesIO(img_data))
                img = img.resize((100, 100), Image.ANTIALIAS)
                img = ImageTk.PhotoImage(img)
                image_label = tk.Label(hotel_frame, image=img)
                image_label.image = img  # Keep reference to the image to prevent garbage collection
                image_label.grid(row=0, column=3, rowspan=2, padx=5)
            else:
                print(f"Failed to fetch image for {hotel['name']}")
        else:
            image_not_available_label = tk.Label(hotel_frame, text="Image not available")
            image_not_available_label.grid(row=0, column=3, rowspan=2, padx=5)

def sort_by_price_low_to_high():
    global hotels
    hotels.sort(key=lambda x: float(x['price'].replace('$', '').replace('Price information not available', '999999')), reverse=False)
    display_hotels(hotels)

def sort_by_price_high_to_low():
    global hotels
    hotels.sort(key=lambda x: float(x['price'].replace('$', '').replace('Price information not available', '999999')), reverse=True)
    display_hotels(hotels)

def sort_by_rating_high_to_low():
    global hotels
    hotels.sort(key=lambda x: float(x['review'].replace('Rating information not available', '-1')), reverse=True)
    display_hotels(hotels)

# Create main window
root = tk.Tk()
root.title("Hotel Information")

# Set minimum window size
root.minsize(800, 500)

# Create a frame for the location entry and button
location_frame = tk.Frame(root)
location_frame.pack(pady=10)

# Create location entry widget
location_label = tk.Label(location_frame, text="Enter City or Country Name:")
location_label.grid(row=0, column=0, padx=5)
location_entry = tk.Entry(location_frame, width=50)
location_entry.grid(row=0, column=1, padx=5)

# Create Scrape button
scrape_button = tk.Button(location_frame, text="Scrape Hotels", command=scrape_hotels)
scrape_button.grid(row=0, column=2, padx=5)

# Create buttons for sorting
sort_price_low_to_high_button = tk.Button(location_frame, text="Sort by Price (Low to High)", command=sort_by_price_low_to_high)
sort_price_low_to_high_button.grid(row=1, column=0, padx=5, pady=5)

sort_price_high_to_low_button = tk.Button(location_frame, text="Sort by Price (High to Low)", command=sort_by_price_high_to_low)
sort_price_high_to_low_button.grid(row=1, column=1, padx=5, pady=5)

sort_rating_high_to_low_button = tk.Button(location_frame, text="Sort by Rating (High to Low)", command=sort_by_rating_high_to_low)
sort_rating_high_to_low_button.grid(row=1, column=2, padx=5, pady=5)

# Create a frame for the treeview
treeview_frame = tk.Frame(root)
treeview_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Run the application
root.mainloop()