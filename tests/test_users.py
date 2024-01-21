import pytest
from API.users import Users  # Replace 'API.user' with the actual path to your Users class

# Sample data for testing
user_data = [
    {"username": "alice", "email": "alice@example.com", "password": "alice123"},
    {"username": "bob", "email": "bob@example.com", "password": "bob123"},
    {"username": "charlie", "email": "charlie@example.com", "password": "charlie123"}
]

# Test user creation
@pytest.mark.parametrize("user", user_data)
def test_create_user(user):
    response, status_code = Users.create_user(user)
    assert status_code == 201
    assert response['username'] == user['username']

# Test authentication
@pytest.mark.parametrize("username_or_email, password, expected_result", [
    ("alice", "alice123", True),
    ("bob@example.com", "bob123", True),
    ("charlie", "wrongpassword", False),
    ("unknown", "nope", False)
])
def test_authenticate_user(username_or_email, password, expected_result):
    result = Users.authenticate_user(username_or_email, password)
    assert result == expected_result

# Test fetching username from email
@pytest.mark.parametrize("email, expected_username", [
    ("alice@example.com", "alice"),
    ("bob@example.com", "bob"),
    ("unknown@example.com", None)
])
def test_get_username_from_email(email, expected_username):
    username = Users.get_username_from_email(email)
    assert username == expected_username

# Test user deletion
@pytest.mark.parametrize("username, expected_result", [
    ("alice", {'message': 'User deleted'}),
    ("unknown", {'message': 'User deleted'})  # Assuming deletion of non-existent user is fine
])
def test_delete_user(username, expected_result):
    response, status_code = Users.delete_user(username)
    assert response == expected_result
