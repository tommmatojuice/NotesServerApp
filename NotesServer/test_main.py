from fastapi.testclient import TestClient

from main import app

global new_id

client = TestClient(app)


def test_get_notes_1():
    """
    Test to check getting all notes:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "note_id": 3,
            "title": "Call Alice",
            "memo": "Ask about the last changes in project",
            "execute_date": "2022-07-15",
            "is_done": False
        }
    ]


def test_post_note():
    """
    Test to check posting a note:

    :return: None
    """
    response = client.post(
        "https://g7gq3p.deta.dev/notes/",
        json={
            "title": "Call Bob",
            "memo": "Ask about the cake",
            "execute_date": "2022-07-02"
        },
    )
    global new_id
    new_id = response.json()["note_id"]
    assert response.status_code == 200
    assert response.json() == {
        "note_id": new_id,
        "title": "Call Bob",
        "memo": "Ask about the cake",
        "execute_date": "2022-07-02",
        "is_done": False
    }


def test_get_notes_2():
    """
    Test to check getting all notes after posting a new one:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "note_id": 3,
            "title": "Call Alice",
            "memo": "Ask about the last changes in project",
            "execute_date": "2022-07-15",
            "is_done": False
        },
        {
            "note_id": new_id,
            "title": "Call Bob",
            "memo": "Ask about the cake",
            "execute_date": "2022-07-02",
            "is_done": False
        }
    ]


def test_post_note_bad_date():
    """
    Test to check posting note with a wrong execute date:

    :return: None
    """
    response = client.post(
        "https://g7gq3p.deta.dev/notes/",
        json={
            "title": "Call Bob",
            "memo": "Ask about the cake",
            "execute_date": "bad date"
        },
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "execute_date"
                ],
                "msg": "invalid date format",
                "type": "value_error.date"
            }
        ]
    }


def test_get_note_by_id():
    """
    Test to check getting a note by ID:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/{new_id}")
    assert response.status_code == 200
    assert response.json() == {
        "note_id": new_id,
        "title": "Call Bob",
        "memo": "Ask about the cake",
        "execute_date": "2022-07-02",
        "is_done": False
    }


def test_get_note_by_id_bad_id():
    """
    Test to check getting a note by ID with a wrong ID:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no note with such id"
    }


def test_make_note_done():
    """
    Test to check marking a note as done by ID:

    :return: None
    """
    response = client.put(f"https://g7gq3p.deta.dev/notes/{new_id}")
    assert response.status_code == 200
    assert response.json() == {
        "note_id": new_id,
        "title": "Call Bob",
        "memo": "Ask about the cake",
        "execute_date": "2022-07-02",
        "is_done": True
    }


def test_make_note_done_bad_id():
    """
    Test to check marking a note as done by ID with wrong ID:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no note with such id"
    }


def test_get_notes_3():
    """
    Test to check getting notes after making one of them done:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "note_id": 3,
            "title": "Call Alice",
            "memo": "Ask about the last changes in project",
            "execute_date": "2022-07-15",
            "is_done": False
        },
        {
            "note_id": new_id,
            "title": "Call Bob",
            "memo": "Ask about the cake",
            "execute_date": "2022-07-02",
            "is_done": True
        }
    ]


def test_delete_note():
    """
    Test to check deleting a note by ID:

    :return: None
    """
    response = client.delete(f"https://g7gq3p.deta.dev/notes/{new_id}")
    assert response.status_code == 200
    assert response.json() == {'message': f'Note was successfully deleted'}


def test_delete_note_bad_id():
    """
    Test to check deleting a note by ID with wrong ID:

    :return: None
    """
    response = client.get(f"https://g7gq3p.deta.dev/notes/0")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no note with such id"
    }
