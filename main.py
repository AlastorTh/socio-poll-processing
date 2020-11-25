import sqlite3
from sqlite3 import Error
import json


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


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.execute("PRAGMA foreign_keys = 1")
        connection.commit()
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("D:\\sm_app.sqlite")


def parse_input(filepath):
    file = open(filepath, "r")
    lines = file.readlines()
    file.close()
    for line in lines:
        line = line.strip()
        line = line.split(", ")
    return lines


with open("input.txt", encoding="UTF-8") as json_file:
    data = json.load(json_file)
    print(data)
# TODO: make a UI, asking for confirmation on every step
create_participants_table = """
CREATE TABLE IF NOT EXISTS participants (
  id_pers INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  sex TEXT,
  education TEXT,
  marital_status TEXT
);
"""

execute_query(connection, create_participants_table)
connection.commit()

for p in data['people']:
    fill_participants = f"""
        INSERT INTO
        participants (name, age, sex, education, marital_status)
        VALUES
        ("{p['name']}", {p['age']}, "{p['sex']}", "{p['university']}", "{p['marital_status']}");"""
    execute_query(connection, fill_participants)

print("Would you like to enter values by hand or from a file?")

create_questions_table = """
CREATE TABLE IF NOT EXISTS questions (
    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
);
"""
execute_query(connection, create_questions_table)

for p in data['questions']:
    fill_questions = f"""
    INSERT INTO
    questions (question)
VALUES
    ("{p['question']}"
    );
    """
    execute_query(connection, fill_questions)

create_form_table = """
CREATE TABLE IF NOT EXISTS forms (
id_form INTEGER PRIMARY KEY AUTOINCREMENT,
id_pers INTEGER,
id_question INTEGER,
answer INTEGER NOT NULL CHECK (answer BETWEEN 1 AND 5),
FOREIGN KEY(id_pers) REFERENCES participants(id_pers),
FOREIGN KEY(id_question) REFERENCES questions(id_question)
);
"""
execute_query(connection, create_form_table)


def fill_forms_row(i, j, ans):
    insert_form_row = f"""

        INSERT INTO
        forms (id_pers, id_question, answer)
    VALUES
        (
            ({j}),
            ({i}),
            ({ans})
        );

    """
    execute_query(connection, insert_form_row)


j = 1
for each in data['people']:
    i = 1
    for ans in each['answers']:
        fill_forms_row(i, j, ans)
        i += 1
    j += 1

