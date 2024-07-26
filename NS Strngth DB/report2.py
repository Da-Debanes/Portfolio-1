import csv
import sqlite3
from datetime import datetime

def connect_db():
    return sqlite3.connect('statuses.db')

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS statuses (
        id INTEGER PRIMARY KEY,
        fourd TEXT NOT NULL,
        name TEXT NOT NULL,
        status TEXT NOT NULL,
        others TEXT,
        expiry_date DATE
    )
    ''')
    conn.commit()
    conn.close()

def insert_status_from_csv(file_path):
    conn = connect_db()
    cursor = conn.cursor()
    
    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            fourd = row['fourd']
            name = row['name']
            status = row['status']
            others = row.get('if others')  # Use `get` to avoid KeyError
            
            # Set expiry_date to None if it is blank, else keep the original value
            expiry_date = row.get('expiry date') or None
            
            # If the status is not 'present' and no expiry date is set, assign today's date
            if status != 'present' and expiry_date is None:
                expiry_date = datetime.today().date()  # Set expiry to today
            
            cursor.execute('INSERT INTO statuses (fourd, name, status, others, expiry_date) VALUES (?, ?, ?, ?, ?)', 
                           (fourd, name, status, others, expiry_date))
    
    conn.commit()
    conn.close()

def update_expired_statuses():
    conn = connect_db()
    cursor = conn.cursor()
    today = datetime.today().date()

    # Update statuses that have expired
    cursor.execute('UPDATE statuses SET status = "present" WHERE expiry_date < ?', (today,))
    conn.commit()
    conn.close()

def get_all_statuses():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT fourd, name, status, others, expiry_date FROM statuses')
    rows = cursor.fetchall()
    conn.close()
    return rows

counts = {
    'total': 0,
    'present': 0,
    'MC': 0,
    'MA': 0,
    'RSI': 0,
    'RSO': 0,
    'Others': 0
}

def counter(rows):
    for row in rows:
        counts['total'] += 1
        status = row[2]  # Adjusted to match the database output
        if status in counts:
            counts[status] += 1
            if status == 'present':
                counts['present'] += 1
        else:
            counts['Others'] += 1  # For statuses not listed explicitly

def print_status_counts_and_names(status, counts, rows):
    if counts[status] == 0:
        print(f"{status}: NIL")
    else:
        print(f'{status}:', counts[status])
        list_indiv(status, rows)

def list_indiv(status, rows):
    for row in rows:
        if row[2] == status:  # Adjusted to match the database output
            name_printer(status, row)

def name_printer(status, row):
    if status == 'Others':
        print('  ', row[0], '-', row[1], ' : ', row[3], sep="")
    else:
        print('  ', row[0], '-', row[1], sep="")

def main():
    create_table()  # Ensure the table exists
    insert_status_from_csv("./file.csv")  # Read from your CSV file

    # Update statuses based on expiry date
    update_expired_statuses()  

    # Fetch all rows from the database
    rows = get_all_statuses()

    # Reset counts
    counts['total'] = 0
    counts['present'] = 0
    for key in counts:
        if key not in ['total', 'present']:
            counts[key] = 0
    
    # Count statuses
    counter(rows)

    # Print results
    print("TOTAL STRENGTH:", counts['total'])
    print("PRESENT STRENGTH:", counts['present'], "\n")

    for stat in ['MC', 'MA', 'RSI', 'RSO', 'Others']:
        print_status_counts_and_names(stat, counts, rows)

if __name__ == "__main__":
    main()