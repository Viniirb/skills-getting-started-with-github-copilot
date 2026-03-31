import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# --- GET /activities ---
def test_get_activities():
    # Arrange & Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# --- POST /activities/{activity_name}/signup ---
def test_signup_for_activity():
    # Arrange
    activity = "Math Olympiad"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

# --- Prevent duplicate signup ---
def test_prevent_duplicate_signup():
    activity = "Science Club"
    email = "testuser2@mergington.edu"
    # Arrange: signup first time
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act: try signup again
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/unregister?email={email}")

# --- DELETE /activities/{activity_name}/unregister ---
def test_unregister_from_activity():
    activity = "Drama Club"
    email = "testuser3@mergington.edu"
    # Arrange: signup
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

# --- Error: unregister non-existent participant ---
def test_unregister_nonexistent_participant():
    activity = "Painting Workshop"
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]

# --- Error: signup for non-existent activity ---
def test_signup_nonexistent_activity():
    activity = "Nonexistent Activity"
    email = "testuser4@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
