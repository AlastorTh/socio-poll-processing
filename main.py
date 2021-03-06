from prettytable import PrettyTable
import sqlite3
from sqlite3 import Error
import json


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        # print("Query executed successfully")
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
        # print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


connection = create_connection("D:\\sm_app.sqlite")

with open("input.json", encoding="UTF-8") as json_file:
    data = json.load(json_file)
print("Welcome to the astounding social poll analyzer v. 1.0(patent pending)")
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


def ans_overall(q_num):
    ans_overall_read = f"""
    SELECT COUNT(*)  FROM forms 
    WHERE forms.id_question = {q_num}
    """
    res = execute_read_query(connection, ans_overall_read)
    return res[0][0]


def ans_specific(q_num, read_ans):
    ans_spec_read = f"""
    SELECT COUNT(*) FROM forms
    WHERE forms.id_question = {q_num}
    AND forms.answer = {read_ans}
"""
    res = execute_read_query(connection, ans_spec_read)
    return res[0][0]


def percentage_distribution(q_num):
    distr = []
    overall_ans = ans_overall(q_num)
    for cnt in range(1, 6):
        ans_n = ans_specific(q_num, cnt)
        distr.append(ans_n / overall_ans)
    return distr


while True:
    action = int(input(
        "1 to clear all tables\n2 to add new data to a table\n3 to view a table \n4 to view percentage distribution\n5 to exit\n"))
    if action == 1:
        while True:
            table_to_clear = int(
                input("1 to clear all tables\n4 to go back to the main page\n"))
            if table_to_clear == 1:
                clear_participants_table = """
                DROP TABLE IF EXISTS participants
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
                break

            elif table_to_clear == 4:
                print("\n")
                break

            else:
                print("Invalid input, try again")

    elif action == 2:
        while True:
            table_to_fill = int(input(
                "Fill the tables:\n1 - participants\n2 - questions\n3 - forms\n4 to go back to menu\n"))

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
                "Table view:\n1 - participants\n2 - questions\n3 - forms\n4 - go back to the menu\n"))

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
        q_num = int(input(
            "Input the question num to get the corresponding percentage distribution:"))
        res = percentage_distribution(q_num)
        print("Answer distribution is:")
        for i in res:
            print(" {:.2f}%".format(i * 100))
    elif action == 5:
        print("\n")
        break

    else:
        print("Invalid input, try again")
