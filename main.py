import sqlite3
from sqlite3 import Error


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


connection = create_connection("D:\\sm_app.sqlite")

# TODO: make a UI, asking for confirmation on every step
create_participants_table = """
CREATE TABLE IF NOT EXISTS participants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  gender TEXT,
  education TEXT,
  marital_status TEXT
);
"""

execute_query(connection, create_participants_table)

# TODO: find a way to add variables to the insert queries
fill_participants = """
INSERT INTO
  participants (name, age, gender, education, marital_status)
VALUES
  ('James', 25, 'male', 'MAI', 'single');
"""

execute_query(connection, fill_participants)

select_participants = "SELECT * from participants"
participants = execute_read_query(connection, select_participants)

for participant in participants:
    print(participant)
