from src.app import activities


def test_signup_adds_student_to_activity(client):
    activity_name = "Chess Club"
    email = "new-student@mergington.edu"

    assert email not in activities[activity_name]["participants"]

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_returns_404_for_unknown_activity(client):
    response = client.post("/activities/Unknown Club/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_student(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_allows_registrations_past_configured_capacity(client):
    activity_name = "Tennis Club"
    max_participants = activities[activity_name]["max_participants"]
    activities[activity_name]["participants"] = [f"student{i}@mergington.edu" for i in range(max_participants)]
    email = "overflow@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]
    assert len(activities[activity_name]["participants"]) == max_participants + 1
