from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_progress():
    response = client.get(
        "/progress/TEST004"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "TEST004"
    assert "overall_mastery" in data
    assert "concepts" in data
    assert "total_attempts" in data
    assert "misconceptions" in data