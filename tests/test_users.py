import pytest
from fastapi.testclient import TestClient


class TestUserCRUD:
    """Test User CRUD operations"""

    def test_create_user(self, client):
        """Test creating a new user"""
        response = client.post(
            "/users/",
            json={"name": "John Doe", "email": "john@example.com"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "John Doe"
        assert data["email"] == "john@example.com"
        assert "id" in data

    def test_create_multiple_users(self, client):
        """Test creating multiple users"""
        user1 = client.post(
            "/users/",
            json={"name": "Alice", "email": "alice@example.com"}
        )
        user2 = client.post(
            "/users/",
            json={"name": "Bob", "email": "bob@example.com"}
        )
        assert user1.status_code == 200
        assert user2.status_code == 200

    def test_get_user(self, client):
        """Test retrieving a user by ID"""
        # First create a user
        create_response = client.post(
            "/users/",
            json={"name": "Jane Doe", "email": "jane@example.com"}
        )
        user_id = create_response.json()["id"]

        # Then retrieve it
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == user_id
        assert data["name"] == "Jane Doe"
        assert data["email"] == "jane@example.com"

    def test_get_nonexistent_user(self, client):
        """Test retrieving a non-existent user"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert response.json()["detail"] == "User not found"

    def test_delete_user(self, client):
        """Test deleting a user"""
        # Create a user
        create_response = client.post(
            "/users/",
            json={"name": "Bob Smith", "email": "bob@example.com"}
        )
        user_id = create_response.json()["id"]

        # Delete the user
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200
        assert delete_response.json()["message"] == "User deleted successfully"

        # Verify user is gone
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_nonexistent_user(self, client):
        """Test deleting a non-existent user"""
        response = client.delete("/users/999")
        assert response.status_code == 404

    def test_get_all_users(self, client):
        """Test retrieving all users"""
        # Create some users
        client.post(
            "/users/",
            json={"name": "User 1", "email": "user1@example.com"}
        )
        client.post(
            "/users/",
            json={"name": "User 2", "email": "user2@example.com"}
        )

        # Get all users
        response = client.get("/users/")
        assert response.status_code == 200
        users = response.json()
        assert len(users) == 2
        assert users[0]["name"] == "User 1"
        assert users[1]["name"] == "User 2"

    def test_get_all_users_empty(self, client):
        """Test retrieving all users when none exist"""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json() == []


class TestUserValidation:
    """Test user validation"""

    def test_create_user_missing_name(self, client):
        """Test creating user without name"""
        response = client.post(
            "/users/",
            json={"email": "john@example.com"}
        )
        assert response.status_code == 422

    def test_create_user_missing_email(self, client):
        """Test creating user without email"""
        response = client.post(
            "/users/",
            json={"name": "John"}
        )
        assert response.status_code == 422


class TestUserWorkflow:
    """Test complete user workflows"""

    def test_full_user_lifecycle(self, client):
        """Test complete lifecycle: create, read, delete"""
        # Create user
        create_response = client.post(
            "/users/",
            json={"name": "Lifecycle User", "email": "lifecycle@example.com"}
        )
        assert create_response.status_code == 200
        user_id = create_response.json()["id"]

        # Read user
        read_response = client.get(f"/users/{user_id}")
        assert read_response.status_code == 200
        assert read_response.json()["name"] == "Lifecycle User"

        # Delete user
        delete_response = client.delete(f"/users/{user_id}")
        assert delete_response.status_code == 200

        # Verify deleted
        final_response = client.get(f"/users/{user_id}")
        assert final_response.status_code == 404

    def test_multiple_users_operations(self, client):
        """Test operations with multiple users"""
        # Create 3 users
        user_ids = []
        for i in range(3):
            response = client.post(
                "/users/",
                json={"name": f"User {i+1}", "email": f"user{i+1}@example.com"}
            )
            user_ids.append(response.json()["id"])

        # Get all users
        all_response = client.get("/users/")
        assert len(all_response.json()) == 3

        # Delete middle user
        delete_response = client.delete(f"/users/{user_ids[1]}")
        assert delete_response.status_code == 200

        # Verify only 2 users remain
        all_response = client.get("/users/")
        assert len(all_response.json()) == 2

        # Verify remaining users are correct
        remaining_ids = [u["id"] for u in all_response.json()]
        assert user_ids[0] in remaining_ids
        assert user_ids[2] in remaining_ids
        assert user_ids[1] not in remaining_ids
