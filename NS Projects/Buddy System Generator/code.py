import sqlite3
import csv

def main():
    db_name = 'personnel.db'
    csv_file = 'Trial1.csv'
    output_csv = 'buddies.csv'

    conn = import_csv_to_db(csv_file, db_name)
    pairs = create_pairs(conn)
    export_pairs_to_csv(pairs, output_csv)
    conn.close()

    print(f"Pairs have been written to {output_csv}")


def import_csv_to_db(csv_file, db_name):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS personnel')
    cur.execute('''
    CREATE TABLE personnel (
        Team TEXT,
        Name TEXT,
        ORD TEXT
    )''')

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = [(row['Team'], row['Name'], row['ORD']) for row in reader]
        cur.executemany('INSERT INTO personnel VALUES (?, ?, ?)', rows)

    conn.commit()
    return conn


def create_pairs(conn):
    cur = conn.cursor()
    cur.execute('''
    SELECT * FROM personnel
    ORDER BY Team,
             (NULLIF(ORD, '') IS NULL) ASC,
             DATE(NULLIF(ORD, '')) ASC
    ''')

    rows = cur.fetchall()

    pairs = []
    pair_counter = {}

    # Relabel Plt 1 to A and Plt 2 to B
    team_labels = {
        'Plt 1': 'A',
        'Plt 2': 'B'
    }

    for row in rows:
        category, name, _ = row
        
        # Relabel Plt 1 to A and Plt 2 to B, keep others as is
        label_prefix = team_labels.get(category, category[0])

        # Initialize pair counter for each category
        if label_prefix not in pair_counter:
            pair_counter[label_prefix] = 1
        
        # Create label with dynamic numbering
        label = f"{label_prefix}{pair_counter[label_prefix]}"
        
        pairs.append((label, name))

        # Increment pair counter every second entry
        if len(pairs) % 2 == 0:
            pair_counter[label_prefix] += 1

    return pairs


def export_pairs_to_csv(pairs, output_csv):
    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['pair', 'name1', 'name2'])
        for i in range(0, len(pairs), 2):
            name1 = pairs[i][1]
            name2 = pairs[i + 1][1] if i + 1 < len(pairs) else ''
            writer.writerow([pairs[i][0], name1, name2])


if __name__ == "__main__":
    main()
