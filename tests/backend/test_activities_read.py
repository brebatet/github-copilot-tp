from src.app import activities


def test_get_activities_returns_current_activity_mapping(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert response.json() == activities


def test_get_activities_items_expose_expected_fields(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()

    assert payload, "Expected at least one activity in payload"

    required_fields = {"description", "schedule", "max_participants", "participants"}
    for activity in payload.values():
        assert required_fields.issubset(activity.keys())
