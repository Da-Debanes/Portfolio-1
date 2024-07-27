from sys import argv
import csv
import sqlite3
from datetime import datetime, timedelta
import os

def main():
    mode = getmode()
    if mode is None:
        return
    
    create_table()
    insert_from_csv("./Restaurants1.csv")
    query(mode)

    delete_db()

def getmode():
    if len(argv) != 2:
        print("Usage: python choose.py [ANNIV|NORM]")
        return None
    
    mode = argv[1].strip().lower()
    if mode not in ['anniv', 'norm']:
        print("INVALID MODE. Select MODE from [ANNIV, NORM]")
        return None
    
    return mode


def connect_db():
    return sqlite3.connect('restaurants.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurants (
        id INTEGER PRIMARY KEY,
        Restaurants TEXT NOT NULL UNIQUE,
        Price INTEGER,
        Rating INTEGER,
        LastVisited DATE
    )
    ''')
    conn.commit()
    conn.close()

def insert_from_csv(filepath):
    conn = connect_db()
    cursor = conn.cursor()
    
    with open(filepath, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            restaurant = row['Restaurants']
            price = int(row['Price'])
            rating = int(row['Rating'])
            last_visited = row.get('LastVisited') or None
            if last_visited:
                last_visited = datetime.strptime(last_visited, "%Y-%m-%d").date()
        
            cursor.execute('SELECT COUNT(*) FROM restaurants WHERE Restaurants = ?', (restaurant,))
            count = cursor.fetchone()[0]
            
            if count == 0:  # Only insert if it does not exist
                cursor.execute('INSERT INTO restaurants (Restaurants, Price, Rating, LastVisited) VALUES (?, ?, ?, ?)',
                               (restaurant, price, rating, last_visited))


    conn.commit()
    conn.close()

def query(mode):
    conn = connect_db()
    cursor = conn.cursor()

    order_by = "Price DESC, Rating DESC" if mode == 'anniv' else "Price ASC, Rating DESC"
    
    today = datetime.today().date()
    one_month_ago = today - timedelta(days=30)
    
    cursor.execute(f'''SELECT Restaurants FROM restaurants
                   WHERE LastVisited IS NULL OR LastVisited <= ? 
                   ORDER BY {order_by}, 
                   RANDOM()
                   LIMIT 10''',
                   (one_month_ago,))
    
    chosen = cursor.fetchall()

    for i, restaurant in enumerate(chosen, start = 1):
        print(f'{i}. {restaurant[0]}')
    
    conn.close()

def delete_db():
    try:
        os.remove('restaurants.db')
    except:
        FileNotFoundError

if __name__ == "__main__":
    main()
