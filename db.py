import sqlite3
import csv
import os

def create_table(cursor, table_name):
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS "{table_name}" (
                        id INTEGER PRIMARY KEY,
                        Name TEXT,
                        Price TEXT,
                        Rating INTEGER,
                        Description TEXT,
                        Link TEXT
                    )''')

def insert_data(cursor, table_name, data):
    cursor.execute(f'''INSERT INTO "{table_name}" (Name, Price, Rating, Description, Link) VALUES (?, ?, ?, ?, ?)''', data)

def load_data_to_database(city_name):
    # Create SQLite database connection
    conn = sqlite3.connect('hotels.db')
    cursor = conn.cursor()

    # Create table if not exists
    create_table(cursor, city_name)

    # Read data from CSV and insert into the database
    with open(f'{city_name}.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            insert_data(cursor, city_name, row)

    # Commit changes and close connection
    conn.commit()
    conn.close()

def main():
    city_names = [
        "Ayodhya"
    ]

    # Load data for each city into the database
    for city_name in city_names:
        print(f"Loading data for {city_name}...")
        load_data_to_database(city_name)

    print("Data loading completed.")

if __name__ == "__main__":
    main()
