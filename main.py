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


# lines = parse_input("input.txt")

# print(lines)

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
# TODO: find a way to add variables to the insert queries

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

fill_question_1 = """
INSERT INTO
    questions (question)
VALUES
    ('To what extent do you agree with the statement A?'
    );
"""
execute_query(connection, fill_question_1)
fill_question_2 = """
INSERT INTO
    questions (question)
VALUES
    (
    'To what extent do you agree with the statement B?'
    );
"""
execute_query(connection, fill_question_2)
fill_question_3 = """
INSERT INTO
    questions (question)
VALUES
    (
    'To what extent do you agree with the statement C?'
    );
"""
execute_query(connection, fill_question_3)
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

fill_form_table = f"""
INSERT INTO
    forms (id_pers, id_question,answer)
VALUES
    (5);
"""

execute_query(connection, fill_form_table)

# command = input()
# if command == "by hand":
#     pass  # TODO: input off keyboard
# elif command == "file":
#     pass  # TODO: input from file
# else:
#     pass  # TODO: error message


select_participants = "SELECT * from participants"
participants = execute_read_query(connection, select_participants)

for participant in participants:
    print(participant)
print("---------------")
select_questions = "SELECT * from questions"
questions = execute_read_query(connection, select_questions)
for question in questions:
    print(question)
print("---------------")
