import pytest

from apps.users.serializers import UserCreateSerializer, UserSerializer
from tests.factories import UserFactory

pytestmark = pytest.mark.django_db


def test_serializer_contains_expected_fields():
    user = UserFactory()
    serializer = UserSerializer(user)
    data = serializer.data
    expected_fields = {
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "bio",
        "telegram",
        "github",
        "total_learning_time",
        "streak_days",
        "created_at",
        "updated_at",
    }
    assert set(data.keys()) == expected_fields


def test_serializer_read_only_fields():
    user = UserFactory()
    serializer = UserSerializer(user)
    read_only_fields = [
        "id",
        "created_at",
        "updated_at",
        "total_learning_time",
        "streak_days",
    ]
    for field in read_only_fields:
        assert field in serializer.data


class TestUserCreateSerializer:
    def test_create_user_valid_data(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpass123",
            "password_confirm": "strongpass123",
        }
        serializer = UserCreateSerializer(data=data)
        assert serializer.is_valid()
        user = serializer.save()
        assert user.username == "newuser"
        assert user.check_password("strongpass123")

    def test_password_mismatch(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "StrongPass123!",
            "password_confirm": "wrong",
        }
        serializer = UserCreateSerializer(data=data)
        assert not serializer.is_valid()
        assert "password_confirm" in serializer.errors
