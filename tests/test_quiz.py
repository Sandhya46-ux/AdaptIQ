from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_quiz_questions():
    response = client.get(
        "/quiz/questions",
        params={
            "concept_id": "C003"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) > 0

    for question in data:
        assert question["concept_id"] == "C003"


def test_submit_quiz():
    payload = {
        "student_id": "TEST002",
        "concept_id": "C003",
        "answers": [
            {
                "question_id": "Q007",
                "answer": "5"
            },
            {
                "question_id": "Q008",
                "answer": "5"
            }
        ]
    }

    response = client.post(
        "/quiz/submit",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["correct"] == 2
    assert data["total"] == 4
    assert data["percentage"] == 50.0
    assert "new_mastery" in data
    assert "next_difficulty" in data