import psycopg2
from psycopg2 import Error


class NotesDB:
    """
    Class describes the database of the application
    """
    def __init__(self):
        """
        Initializing a connection to the database
        """
        try:
            self.connection = psycopg2.connect(user="mcrufqdw",
                                               password="VnF4vV2FsNRexEtya3PUoEBkNHKlHX10",
                                               host="tyke.db.elephantsql.com",
                                               port="5432",
                                               database="mcrufqdw")
            self.cursor = self.connection.cursor()
            self.cursor.execute("SELECT version();")
            print("You're connected to - ", self.cursor.fetchone(), "\n")

            self.create_table()

        except (Exception, Error) as error:
            print("Server connection error", error)

    def create_table(self):
        """
        Creating the table 'note' in database:

        :return: None
        """
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
        """
        Getting all notes:

        :return: list of tuples with notes
        """
        try:
            get_notes_query = f'SELECT * FROM note;'

            self.cursor.execute(get_notes_query)
            return self.cursor.fetchall()

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def add_note(self, note):
        """
        Inserting new note:

        :param note: object of class Note
        :return: note as a tuple
        """
        try:
            add_note_query = 'INSERT INTO note(title, memo, execute_date, is_done) ' \
                             'VALUES (%s,%s,%s,%s) RETURNING note_id;'
            self.cursor.execute(add_note_query, (note.title, note.memo,
                                                 note.execute_date, False))
            self.connection.commit()
            return self.cursor.fetchone()[0]

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def get_note_by_id(self, note_id):
        """
        Getting note by id:

        :param note_id: note ID
        :return: note as a tuple
        """
        try:
            get_note_query = f'SELECT * FROM note WHERE note_id = %s;'

            self.cursor.execute(get_note_query, (note_id,))
            return self.cursor.fetchall()[0]

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def make_note_done(self, note_id):
        """
        Marking note as done:

        :param note_id: note ID
        :return: note as a tuple
        """
        try:
            update_note_query = f'UPDATE note SET is_done = True WHERE note_id = %s;'

            self.cursor.execute(update_note_query, (note_id,))
            self.connection.commit()

            return self.cursor.fetchall()

        except (Exception, Error) as error:
            print("Error while getting data", error)

    def delete_note(self, note_id):
        """
        Deleting a note:

        :param note_id: note ID
        :return: None
        """
        try:
            delete_note_query = f'DELETE FROM note WHERE note_id = %s'

            self.cursor.execute(delete_note_query, (note_id,))
            self.connection.commit()

        except (Exception, Error) as error:
            print("Error while deleting data", error)

    def check_note_id(self, note_id):
        """
        Checking existence of note ID:

        :param note_id: note ID
        :return: boolean value of existence
        """
        try:
            get_note_query = f'SELECT * FROM note WHERE note_id = %s;'

            self.cursor.execute(get_note_query, (note_id,))
            return True if self.cursor.fetchall()[0] else False

        except (Exception, Error) as error:
            print("Error while getting data", error)
