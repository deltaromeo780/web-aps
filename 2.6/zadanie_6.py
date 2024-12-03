import psycopg2
from faker import Faker
import random

fake = Faker()


class DatabaseManager:
    def __init__(self, uri):
        self.uri = uri
        self.connection = psycopg2.connect(uri)
        self.cursor = self.connection.cursor()

    def create_groups_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS groups (
                 id SERIAL PRIMARY KEY,
                 name VARCHAR(255) NOT NULL
                );
            """
        )

    def create_students_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                "group_id" INTEGER NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id)
                );
            """
        )

    def create_lecturers_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS lecturers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL
                );
            """
        )

    def create_subjects_table(self):
        self.cursor.execute(
            """
             CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                "lecturer_id" INTEGER NOT NULL,
                FOREIGN KEY (lecturer_id) REFERENCES lecturers(id)
                );
            """
        )

    def create_grades_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS grades (
                id SERIAL PRIMARY KEY,
                value REAL NOT NULL,
                date DATE NOT NULL,
                "student_id" INTEGER NOT NULL,
                "subject_id" INTEGER NOT NULL,
                FOREIGN KEY (student_id) REFERENCES students(id),
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
                );
            """
        )

    def insert_group_data(self, group_names):
        for name in group_names:
            self.cursor.execute('INSERT INTO groups (name) VALUES (%s)', (name,))

    def insert_student_data(self, num_students):
        for _ in range(num_students):
            self.cursor.execute('INSERT INTO students (name, group_id) VALUES (%s, %s)',
                                (fake.name(), random.randint(1, 3)))

    def insert_lecturer_data(self, num_lecturers):
        for _ in range(num_lecturers):
            self.cursor.execute('INSERT INTO lecturers (name) VALUES (%s)', (fake.name(),))

    def insert_subject_data(self, subject_names, num_lecturers):
        for name in subject_names:
            self.cursor.execute('INSERT INTO subjects (name, lecturer_id) VALUES (%s, %s)',
                                (name, random.randint(1, num_lecturers)))

    def insert_grade_data(self, num_students, num_subjects):
        for student_id in range(1, num_students + 1):
            for subject_id in range(1, num_subjects + 1):
                for _ in range(random.randint(1, 5)):
                    self.cursor.execute('INSERT INTO grades (student_id, subject_id, value, date) VALUES (%s, %s, %s, %s)',
                                       (student_id, subject_id, random.randint(2, 5), fake.date_this_year()))

    def commit_and_close(self):
        self.connection.commit()
        self.connection.close()


if __name__ == "__main__":
    uri = "postgresql://admin:password@localhost:5432/my_database"
    db_manager = DatabaseManager(uri)

    db_manager.create_groups_table()
    db_manager.create_students_table()
    db_manager.create_lecturers_table()
    db_manager.create_subjects_table()
    db_manager.create_grades_table()

    group_names = ['Group A', 'Group B', 'Group C']
    db_manager.insert_group_data(group_names)

    num_students = 30
    db_manager.insert_student_data(num_students)

    num_lecturers = 3
    db_manager.insert_lecturer_data(num_lecturers)

    subject_names = ['Math', 'Physics', 'Chemistry', 'Biology', 'History', 'English', 'Computer Science']
    db_manager.insert_subject_data(subject_names, num_lecturers)

    db_manager.insert_grade_data(num_students, len(subject_names))

    db_manager.commit_and_close()
