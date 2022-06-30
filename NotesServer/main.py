from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from db_connection import NotesDB
from note import NoteOut, NoteIn, Note

app = FastAPI()
db = NotesDB()

TIME_FORMAT = '%Y-%m-%d'


def get_note(note_id):
    """
    Getting note by id as an object of class Note:

    :param note_id: note id
    :return: object of class Note
    """
    reply = db.get_note_by_id(note_id)
    return Note(reply[0], reply[1], reply[2], reply[3].strftime(TIME_FORMAT), reply[4]).__dict__


@app.post("/notes/", response_model=NoteOut)
async def post_note(note: NoteIn):
    """
    API for posting a note:

    :param note: object of class NoteIn
    :return: object of class NoteOut
    """
    try:
        note_id = db.add_note(note)
        return get_note(note_id)

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error posting the note")


@app.get("/notes/", response_model=List[NoteOut])
async def get_notes():
    """
    API for getting all notes:

    :return: list of object of class NoteOut
    """
    try:
        result = [Note(note[0], note[1], note[2], note[3].strftime(TIME_FORMAT), note[4]).__dict__
                  for note in db.get_notes()]
        return result

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error getting the note")


@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note_by_id(note_id: int):
    """
    API for getting a note by ID:

    :param note_id: note ID
    :return: object of class NoteOut
    """
    if not db.check_note_id(note_id):
        raise HTTPException(status_code=404, detail="There is no note with such id")
    else:
        try:
            return get_note(note_id)
        except Exception:
            raise HTTPException(status_code=500, detail="There was an error getting the note")


@app.put("/notes/{note_id}", response_model=NoteOut)
async def set_note_done(note_id: int):
    """
    API for marking a note as done by ID:

    :param note_id: note ID
    :return: object of class NoteOut
    """
    if not db.check_note_id(note_id):
        raise HTTPException(status_code=404, detail="There is no note with such id")
    else:
        try:
            db.make_note_done(note_id)
            return get_note(note_id)
        except Exception:
            raise HTTPException(status_code=500, detail="There was an error changing the note")


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    """
    API for deleting a note by ID:

    :param note_id: note ID
    :return: message about the success
    """
    if not db.check_note_id(note_id):
        raise HTTPException(status_code=404, detail="There is no note with such id")
    else:
        try:
            db.delete_note(note_id)
            return {'message': f'Note was successfully deleted'}
        except Exception:
            raise HTTPException(status_code=500, detail="There was an error deleting the note")


if __name__ == '__main__':
    """
    Main function to run application on localhost:8000
    """
    uvicorn.run(app, host='localhost', port=8000)
