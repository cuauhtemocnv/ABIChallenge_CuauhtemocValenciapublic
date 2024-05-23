import sqlite3

def view_entries(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query all entries from the Prediction table
    cursor.execute("SELECT * FROM Prediction")

    # Fetch all rows from the executed query
    rows = cursor.fetchall()

    # Print the column names
    column_names = [description[0] for description in cursor.description]
    print(" | ".join(column_names))

    # Print each row
    for row in rows:
        print(" | ".join(map(str, row)))

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    db_path = 'db.sqlite3'  # Path to your SQLite database file
    view_entries(db_path)
