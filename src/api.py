from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException
from db_connection import NotesDB
from note import NoteOut, NoteIn, Note

app = FastAPI()
db = NotesDB()

TIME_FORMAT = '%Y-%m-%d'


@app.post("/notes/", response_model=NoteOut)
async def post_note(note: NoteIn):
    try:
        print(note.execute_date)
        note_id = db.add_note(note)

        reply = db.get_note_by_id(note_id)
        return Note(reply[0], reply[1], reply[2], reply[3].strftime(TIME_FORMAT)).__dict__

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error posting the note")


@app.get("/notes/", response_model=List[NoteOut])
async def get_notes():
    try:
        result = [Note(note[0], note[1], note[2], note[3].strftime(TIME_FORMAT)).__dict__
                  for note in db.get_notes()]
        return result

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error getting the note")


@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note_by_id(note_id: int):
    try:
        reply = db.get_note_by_id(note_id)
        return Note(reply[0], reply[1], reply[2], reply[3].strftime(TIME_FORMAT)).__dict__

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error getting the note")


@app.put("/notes/{note_id}", response_model=NoteOut)
async def set_note_done(note_id: int):
    try:
        db.check_note(note_id)
        reply = db.get_note_by_id(note_id)
        return Note(reply[0], reply[1], reply[2], reply[3].strftime(TIME_FORMAT), reply[4]).__dict__

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error changing the note")


@app.delete("/notes/{note_id}")
async def delete_note(note_id: int):
    try:
        db.delete_note(note_id)
        return {'message': f'Note was successfully deleted'}

    except Exception:
        raise HTTPException(status_code=500, detail="There was an error deleting the note")

if __name__ == '__main__':
    uvicorn.run(app, host='localhost', port=8000)
