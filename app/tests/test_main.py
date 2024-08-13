import time
from fastapi.testclient import TestClient
from main import app  # Абсолютный импорт


client = TestClient(app)


def test_read_main():
    expected_names = [
        "attendance-employee",
        "attendance-student",
        "department",
        "group",
        "managment",
        "psychology-employee",
        "psychology-student",
        "role",
        "room",
        "student",
        "subject",
        "teacher",
        "timetable",
    ]

    start_time = time.time()
    response = client.get("/resources/")
    elapsed_time = time.time() - start_time

    assert response.status_code == 200
    assert elapsed_time < 0.06, f"Request took too long: {elapsed_time} seconds"
    try:
        data = response.json()
    except ValueError:
        assert False, "Response body is not a valid JSON"

    assert isinstance(data, list), "Response is not a list"

    assert len(data) == 13, "Unexpected number of items in the response"

    actual_names = [item["name"] for item in data]

    assert sorted(actual_names) == expected_names, "Names do not match expected values"

    for item in data:
        assert isinstance(item, dict), "Each item should be a dictionary"
        assert "name" in item, "Each item should have a 'name' key"
        assert "id" in item, "Each item should have an 'id' key"
        assert isinstance(item["name"], str), "'name' should be a string"
        assert isinstance(item["id"], str), "'id' should be a string"
