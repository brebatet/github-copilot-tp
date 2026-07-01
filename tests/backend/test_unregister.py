from src.app import activities


def test_unregister_removes_student_from_activity(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    assert email in activities[activity_name]["participants"]

    response = client.delete(f"/activities/{activity_name}/unregister", params={"email": email})

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"


def test_unregister_returns_404_for_unknown_activity(client):
    response = client.delete("/activities/Unknown Club/unregister", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_when_student_not_enrolled(client):
    response = client.delete("/activities/Chess Club/unregister", params={"email": "new@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in this activity"
