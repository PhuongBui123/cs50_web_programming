# (1) Query data from students.db by Python (i.e writing SQL via Python script)
# (2) Use Python script to print the result

from sys import argv, exit
import sqlite3

# Remember to call mall() at the end of this script


def main():
    # Check command-line arguments
    if len(argv) != 2:
        print("Usage: python roster.py house_name")
        exit(1)
    else:
        data = query(argv[1])
        ##-- Checking --##
        #print("store =",query(house))

        ##-- Result --##
        print(result(data))
        exit(0)


def query(house):
    # Connect to available database
    conn = sqlite3.connect('students.db')
    # Set up a cursor to work with the above connection
    c = conn.cursor()

    # SQL script is executed here
    script = '''
    SELECT first, middle, last, birth FROM students
    WHERE house = '{}'
    ORDER BY last, first
    '''
    c.execute(script.format(house))

    # Save (commit) the changes
    conn.commit()

    store = c.fetchall()
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    return store


def result(data):
    store = ""
    for row in data:
        n = len(row)
        for i in range(n):
            # Generalize all the length of rows
            if row[i] == None:
                continue
            elif i == 0:
                store += row[i]
            elif i == (n - 1):
                store += ", born " + str(row[i]) + "\n"
            else:
                store += " " + row[i]
    # use .rstrip("\n") to remove the final "\n" of the string
    return store.rstrip("\n")


##-- Main --##
main()
