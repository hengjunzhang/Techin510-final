import sqlite3
from datetime import datetime

def create_connection(db_file):
    """Create a database connection to a SQLite database specified by db_file"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn):
    """Create a table to store user inputs"""
    sql_create_user_inputs_table = """ CREATE TABLE IF NOT EXISTS user_inputs (
                                        id integer PRIMARY KEY,
                                        age integer NOT NULL,
                                        weight real NOT NULL,
                                        height real NOT NULL,
                                        body_fat_percentage real,
                                        gender text NOT NULL,
                                        activity_level text NOT NULL,
                                        goal text NOT NULL,
                                        timestamp datetime NOT NULL
                                    ); """
    try:
        c = conn.cursor()
        c.execute(sql_create_user_inputs_table)
    except sqlite3.Error as e:
        print(e)
def insert_user_input(conn, user_data):
    """
    Insert a new user input into the user_inputs table
    :param conn: Connection object to the SQLite database
    :param user_data: A tuple containing user data to insert
    """
    sql = ''' INSERT INTO user_inputs(age, weight, height, body_fat_percentage, gender, activity_level, goal, timestamp)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user_data)
    conn.commit()
# Example usage
db_file = "user_data.db"
conn = create_connection(db_file)
if conn is not None:
    create_table(conn)
else:
    print("Error! cannot create the database connection.")

