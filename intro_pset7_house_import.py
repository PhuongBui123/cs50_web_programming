# Insert data from characters.csv to students.db
from sys import argv, exit
from csv import DictReader
import sqlite3

# Remember to call mall() at the end of this script


def main():
    # Check command-line arguments
    if len(argv) != 2:
        print("Usage: python import.py characters.csv")
        exit(1)
    else:
        file = argv[1]
        data = load_csv(file)
        transfer(data)
        exit(0)

# Load the csv file and write in a dictionary


def load_csv(file):
    data = dict()
    # Load to csv to memory:
    with open(file, 'r') as csv_file:
        file_read = DictReader(csv_file, delimiter=",")
        name, house, birth = list(), list(), list()
        # house = list()
        # birth = list()
        for row in file_read:
            name.append(row['name'])
            house.append(row['house'])
            birth.append(row['birth'])
        # Insert values to expected keys of the "data" dictionary
        data['name'] = name
        data['house'] = house
        data['birth'] = birth
    return data

# Break the name into a tuple of 3 values including "first", "middle", "last" names


def seperate(name):
    temp_dict = dict()
    # Split the name to a list
    store = name.split(" ")
    # Insert values to the dictionary
    temp_dict['first'] = store[0]
    temp_dict['last'] = store[-1]
    if len(store) > 2:
        temp_dict['middle'] = store[1]
    else:
        temp_dict['middle'] = None

    return temp_dict

# Transfer data from dictionary to students.db
# Insert the students' info into the students table in the students.db database


def transfer(data):
    # Connect to available database
    conn = sqlite3.connect('students.db')
    # Set up a cursor to work with the above connection
    c = conn.cursor()

    # Initialize n to identify the number of lines to insert run row by row
    n = len(data['name'])
    row = 0

    # Run a loop to insert each student's info into "students" table in students.db
    while row < n:
        name = data['name'][row]
        first = seperate(name)['first']
        middle = seperate(name)['middle']
        if middle == "None":
            middle = None
        last = seperate(name)['last']
        house = data['house'][row]
        birth = data['birth'][row]
        # Insert data from dictionary to table of database
        # Be careful with syntax of SQL in the string!
        # Use .format() will make NULL values converted to strings in SQL
        c.execute("INSERT INTO students VALUES (?,?,?,?,?,?)", (row, first, middle, last, house, int(birth)))
        row += 1

    # Save (commit) the changes
    conn.commit()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()


##-- Main -- ###
main()
