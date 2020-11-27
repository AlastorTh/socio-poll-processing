from prettytable import PrettyTable
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

create_questions_table = """
CREATE TABLE IF NOT EXISTS questions (
    id_question INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL
);
"""
execute_query(connection, create_questions_table)

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
while True:
    action = int(input(
        "If you want to :\n clear all tables - press 1\n add new data to a table  - press 2\n see a table - press 3\n to exit - press 4\n"))
    if action == 1:
        while True:
            table_to_clear = int(input("If you want to clear all tables - press 1\n to skip - press 4\n"))
            if table_to_clear == 1:
                clear_participants_table = """
                DROP TABLE IF EXISTS participants
                ;
                """
                execute_query(connection, clear_participants_table)
                execute_query(connection, create_participants_table)

                clear_questions_table = """
                DROP TABLE IF EXISTS questions
                ;
                """
                execute_query(connection, clear_questions_table)
                execute_query(connection, create_questions_table)

                clear_forms_table = """
                DROP TABLE IF EXISTS forms
                ;
                """
                execute_query(connection, clear_forms_table)
                execute_query(connection, create_form_table)

            elif table_to_clear == 4:
                print("\n")
                break

            else:
                print("Invalid input, try again")

    elif action == 2:
        while True:
            table_to_fill = int(input(
                "If you want to add new data to:\n participants table - press 1\n questions table - press 2\n forms table - press 3\n to exit - press 4\n"))

            if table_to_fill == 1:
                for p in data['people']:
                    fill_participants = f"""
                        INSERT INTO
                        participants (name, age, sex, education, marital_status)
                        VALUES
                        ("{p['name']}", {p['age']}, "{p['sex']}", "{p['university']}", "{p['marital_status']}");"""
                    execute_query(connection, fill_participants)



            elif table_to_fill == 2:
                for p in data['questions']:
                    fill_questions = f"""
                    INSERT INTO
                    questions (question)
                VALUES
                    ("{p['question']}"
                    );
                    """
                    execute_query(connection, fill_questions)


            elif table_to_fill == 3:
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
            elif table_to_fill == 4:
                print("\n")
                break
            else:
                print("Invalid input, try again")

    elif action == 3:
        while True:
            table_to_show = int(input(
                "If you want to see:\n participants table - press 1\n questions table - press 2\n forms table - press 3\n to exit - press 4\n"))

            if table_to_show == 1:

                table = PrettyTable()

                table.field_names = ["ID", "Name", "Age",
                                     "Sex", "Education", "Marital status"]

                query = """SELECT * FROM participants"""
                t = execute_read_query(connection, query)

                for i in range(len(t)):
                    table.add_row(
                        [t[i][0], t[i][1], t[i][2], t[i][3], t[i][4], t[i][5]])

                print(table)


            elif table_to_show == 2:

                table = PrettyTable()

                table.field_names = ["ID", "Question"]

                query = """SELECT * FROM questions"""
                t = execute_read_query(connection, query)

                for i in range(len(t)):
                    table.add_row([t[i][0], t[i][1]])

                print(table)


            elif table_to_show == 3:

                table = PrettyTable()

                table.field_names = [
                    "ID", "Name of the person ", "Question", "Answer"]

                query = """
                SELECT f.id_form, p.name, q.question, f.answer
                FROM 'forms' f
                INNER JOIN 'participants' p ON p.id_pers     = f.id_pers
                INNER JOIN 'questions'    q ON q.id_question = f.id_question """

                t = execute_read_query(connection, query)

                for i in range(len(t)):
                    table.add_row([t[i][0], t[i][1], t[i][2], t[i][3]])

                print(table)

            elif table_to_show == 4:
                print("\n")
                break

            else:
                print("Invalid input, try again")

    elif action == 4:
        print("\n")
        break

    else:
        print("Invalid input, try again")
