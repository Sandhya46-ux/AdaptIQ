from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_diagnostic_submission():
    payload = {
        "student_id": "TEST001",
        "answers": [
            {
                "question_id": "Q001",
                "answer": "3/4"
            },
            {
                "question_id": "Q002",
                "answer": "1/2"
            },
            {
                "question_id": "Q003",
                "answer": "4/10"
            }
        ]
    }

    response = client.post(
        "/diagnostic/submit",
        json=payload
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "TEST001"
    assert data["score"] == 2
    assert data["total"] == 3
    assert data["percentage"] == 66.67
    assert "C001" in data["mastery"]