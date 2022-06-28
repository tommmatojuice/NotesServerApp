from pydantic import BaseModel, Field
from datetime import date


class Note:
    def __init__(self, note_id, title, memo, execute_date, is_executed=False):
        self.note_id = note_id
        self.title = title
        self.memo = memo
        self.execute_date = execute_date
        self.is_executed = is_executed


class NoteIn(BaseModel):
    title: str = Field(example="Call Alice")
    memo: str = Field(example="Ask about the last changes in project")
    execute_date: date = Field(example="2022-07-15")


class NoteOut(BaseModel):
    title: str
    memo: str
    execute_date: date
    is_executed: bool
