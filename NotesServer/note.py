from pydantic import BaseModel, Field
from datetime import date


class Note:
    """
    Class describes the structure of a note
    """

    def __init__(self, note_id: int, title: str, memo: str, execute_date: date, is_done: bool = False):
        """
        Initializing a note:

        :param note_id: note ID
        :param title: note title
        :param memo: note description
        :param execute_date: planed date to execute the task
        :param is_done: flag shows if the note id done
        """
        self.note_id = note_id
        self.title = title
        self.memo = memo
        self.execute_date = execute_date
        self.is_done = is_done


class NoteIn(BaseModel):
    """
    Class describes the structure of a note in a request
    """
    title: str = Field(example="Call Alice")
    memo: str = Field(example="Ask about the last changes in project")
    execute_date: date = Field(example="2022-07-15")


class NoteOut(BaseModel):
    """
    Class describes the structure of a note as a return value
    """
    note_id: int
    title: str
    memo: str
    execute_date: date
    is_done: bool = False
