from unittest.mock import Mock, patch

from my_validation.datamodel import User, UserDict
from my_validation.service import fetch_user_data, filter_active_users, validate_users


def test_validate_users() -> None:
    """
    Tests that validate_users correctly filters out invalid data.
    """
    users_data: list[UserDict] = [
        {"id": 1, "name": "Alice", "is_active": True},  # valid
        {"id": None, "name": "Bob", "is_active": False},  # invalid id
        {"id": 3, "name": "", "is_active": True},  # invalid name
        {"id": -4, "name": "Charlie", "is_active": True},  # invalid negative id
        {"id": 4, "name": "David", "is_active": True},  # valid
    ]

    valid_users = validate_users(users_data)

    # 검증이 통과된 사용자만 남아야 함
    assert len(valid_users) == 2
    assert valid_users[0].name == "Alice"
    assert valid_users[1].name == "David"


def test_filter_active_users() -> None:
    """
    Tests that filter_active_users correctly filters only active users.
    """
    users: list[User] = [
        User(id=1, name="Alice", is_active=True),
        User(id=2, name="Bob", is_active=False),
        User(id=3, name="Charlie", is_active=True),
    ]

    result: list[User] = filter_active_users(users)

    assert len(result) == 2
    assert result[0].name == "Alice"
    assert result[1].name == "Charlie"


def test_fetch_and_validate_users() -> None:
    """
    Tests the complete flow of fetching and validating user data, including invalid cases.
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"id": 1, "name": "Alice", "is_active": True},
        {"id": None, "name": "Bob", "is_active": False},  # invalid
        {"id": 3, "name": "", "is_active": True},  # invalid
        {"id": -4, "name": "Charlie", "is_active": True},  # invalid negative id
        {"id": 4, "name": "David", "is_active": True},  # valid
    ]

    with patch("requests.get", return_value=mock_response):
        url = "http://example.com/api/users"
        users_data = fetch_user_data(url)
        valid_users = validate_users(users_data)
        active_users = filter_active_users(valid_users)

        assert len(active_users) == 2
        assert active_users[0].name == "Alice"
        assert active_users[1].name == "David"