from bs4 import BeautifulSoup
import csv
import requests
import urllib.parse

# List of cities
cities = ["Ayodhya"]

# Loop over each city
for city_name in cities:
    city_name_encoded = urllib.parse.quote(city_name)
    url = f"https://www.google.com/travel/search?q={city_name_encoded}%20hotels&qs=OAA&ved=0CAAQ5JsGahcKEwjQsqTK_umEAxUAAAAAHQAAAAAQCw"
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")
    hotels = soup.find_all("div", class_="uaTTDe BcKagd bLc2Te Xr6b1e")

    csv_filename = city_name.replace(" ", "_")

    with open(f"{csv_filename}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Name", "Price", "Rating", "Description", "Booking Link"])
        
        for hotel in hotels:
            name_element = hotel.find("h2", class_="BgYkof ogfYpf ykx2he")
            price_element = hotel.find("span", jsaction="mouseenter:JttVIc;mouseleave:VqIRre;")
            review_element = hotel.find("span", class_="KFi5wf lA0BZ")
            description_element = hotel.find("span", class_="lXJaOd")
            
            booking_link_element = hotel.find("a", class_="aS3xV lRagtb xl0RMe")
            booking_link = "https://www.google.com" + booking_link_element["href"] if booking_link_element else "Booking link not available"

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

                writer.writerow([name, price, review, description, booking_link])

    print(f"Data saved to {csv_filename}.csv")