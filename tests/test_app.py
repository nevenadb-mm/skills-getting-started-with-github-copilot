import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test: Viewing activities

def test_view_activities():
    # Arrange: None needed, uses in-memory DB
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

# Test: Signing up for an activity (success)

def test_signup_activity_success():
    # Arrange
    signup_data = {"activity": "Chess Club", "email": "newstudent@mergington.edu"}
    # Act
    response = client.post("/signup", json=signup_data)
    # Assert
    assert response.status_code == 200
    assert response.json()["message"].startswith("Signed up")

# Test: Signing up for an activity (max participants error)

def test_signup_activity_max_participants():
    # Arrange
    activity = "Chess Club"
    # Fill up participants
    for i in range(10):
        client.post("/signup", json={"activity": activity, "email": f"student{i}@mergington.edu"})
    # Act
    response = client.post("/signup", json={"activity": activity, "email": "overflow@mergington.edu"})
    # Assert
    assert response.status_code == 400
    assert "max participants" in response.json()["detail"]
