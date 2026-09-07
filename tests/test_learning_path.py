from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_learning_path():
    response = client.get(
        "/learning-path/TEST003"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["student_id"] == "TEST003"
    assert "learning_path" in data
    assert isinstance(
        data["learning_path"],
        list
    )