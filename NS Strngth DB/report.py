import csv

def main():
    with open("./file.csv", "r") as file:
        reader = csv.DictReader(file)

        rows = list(reader)

        counter(rows)
    
        print("TOTAL STRENGTH:", counts['total'])
        print("PRESENT STRENGTH:", counts['present'], "\n")

        for stat in ['MC', 'MA', 'RSI', 'RSO', 'Others']:
            print_status_counts_and_names(stat, counts, rows)

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
        status = row['status']
        if status in counts:
            counts[status] += 1
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
            if row['status'] == status:
                  name_printer(status, row)
                
def name_printer(status, row):
    if status == 'Others':
        print('  ', row['fourd'], '-', row['name'], ' : ', row['if others'], sep = "")
    else:
        print('  ', row['fourd'], '-', row['name'], sep = "")

if __name__ == "__main__":
    main()

