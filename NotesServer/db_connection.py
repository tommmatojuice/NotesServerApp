import psycopg2
from psycopg2 import Error


class NotesDB:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(user="mcrufqdw",
                                               password="VnF4vV2FsNRexEtya3PUoEBkNHKlHX10",
                                               host="tyke.db.elephantsql.com",
                                               port="5432",
                                               database="mcrufqdw")
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You're connected to - ", record, "\n")

            self.create_table()

        except (Exception, Error) as error:
            print("Server connection error", error)

    def create_table(self):
        try:
            create_table_query = ('CREATE TABLE IF NOT EXISTS note (\n'
                                  '                            note_id SERIAL PRIMARY KEY,\n'
                                  '                            title varchar(100) NOT NULL,\n'
                                  '                            memo varchar(500) NOT NULL,\n'
                                  '                            execute_date date NOT NULL,\n'
                                  '                            is_done bool NOT NULL\n'
                                  '                            );')

            self.cursor.execute(create_table_query)
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error creating table", error)

    def get_notes(self):
        try:
            get_notes_query = f'SELECT * FROM note;'

            self.cursor.execute(get_notes_query)
            record = self.cursor.fetchall()

            return record

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def add_note(self, note):
        try:
            add_note_query = 'INSERT INTO note(title, memo, execute_date, is_done) ' \
                             'VALUES (%s,%s,%s,%s) RETURNING note_id;'
            self.cursor.execute(add_note_query, (note.title, note.memo,
                                                 note.execute_date, False))
            self.connection.commit()
            record = self.cursor.fetchone()[0]

            return record

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def get_note_by_id(self, note_id):
        try:
            get_note_query = f'SELECT * FROM note WHERE note_id = %s;'

            self.cursor.execute(get_note_query, (note_id,))
            record = self.cursor.fetchall()[0]

            return record

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def make_note_done(self, note_id):
        try:
            update_note_query = f'UPDATE note SET is_done = True WHERE note_id = %s;'

            self.cursor.execute(update_note_query, (note_id,))
            self.connection.commit()
            record = self.cursor.fetchall()

            return record

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def delete_note(self, note_id):
        try:
            delete_note_query = f'DELETE FROM note WHERE note_id = %s'

            self.cursor.execute(delete_note_query, (note_id,))
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while deleting data", error)

    def check_note_id(self, note_id):
        try:
            get_note_query = f'SELECT * FROM note WHERE note_id = %s;'

            self.cursor.execute(get_note_query, (note_id,))
            record = self.cursor.fetchall()[0]
            print(record)

            return True if record else False

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def get_last_id(self):
        try:
            get_note_query = f'SELECT MAX(note_id) FROM note;'

            self.cursor.execute(get_note_query)
            record = self.cursor.fetchall()[0]

            return record[0]

        except (Exception, Error) as error:
            print("Error while getting data", error)
