import sqlite3

def create_city_table():
    conn = sqlite3.connect('hotels.db')
    cursor = conn.cursor()
    try:
        # Create the city table if it does not exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS city (
                            id INTEGER PRIMARY KEY,
                            name TEXT
                        )''')

        # List of cities
        cities = ["Mumbai", "Delhi", "Bangalore", "Kolkata", "Chennai", "Hyderabad", "Ahmedabad", "Pune", "Surat", "Jaipur",
                  "Lucknow", "Kanpur", "Nagpur", "Visakhapatnam", "Indore", "Thane", "Bhopal", "Patna", "Vadodara", "Ghaziabad",
                  "Ludhiana", "Agra", "Nashik", "Ranchi", "Faridabad", "Meerut", "Rajkot", "Kalyan_Dombivali", "Vasai_Virar",
                  "Varanasi", "Srinagar", "Aurangabad", "Dhanbad", "Amritsar", "Navi_Mumbai", "Allahabad", "Howrah", "Gwalior",
                  "Jabalpur", "Coimbatore", "Vijayawada", "Jodhpur", "Madurai", "Raipur", "Kota", "Chandigarh", "Guwahati",
                  "Solapur", "Hubli_Dharwad", "Bareilly", "Moradabad", "Mysore", "Gurgaon", "Aligarh", "Jalandhar", "Tiruchirappalli",
                  "Bhubaneswar", "Salem", "Mira_Bhayandar", "Warangal", "Thiruvananthapuram", "Guntur", "Bhiwandi", "Saharanpur",
                  "Gorakhpur", "Bikaner", "Amravati", "Noida", "Jamshedpur", "Bhilai", "Cuttack", "Firozabad", "Kochi",
                  "Nellore", "Bhavnagar", "Dehradun", "Durgapur", "Asansol", "Rourkela", "Nanded", "Kolhapur", "Ajmer",
                  "Akola", "Gulbarga", "Jamnagar", "Ujjain", "Loni", "Siliguri", "Jhansi", "Ulhasnagar", "Jammu"]

        # Insert the cities into the table
        for city in cities:
            cursor.execute("INSERT INTO city (name) VALUES (?)", (city,))
        
        # Commit the changes and close the connection
        conn.commit()
        conn.close()
        print("City table created and populated successfully.")
    except sqlite3.Error as e:
        print("Error:", e)

if __name__ == "__main__":
    create_city_table()
