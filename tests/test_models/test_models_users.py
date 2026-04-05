import pytest
from django.contrib.auth import get_user_model
from django.db import IntegrityError

from apps.users.models import UserRole

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestUserModel:
    def test_create_student_user(self):
        user = User.objects.create_user(
            username="student1",
            email="student@example.com",
            password="testpass123",
            role=UserRole.STUDENT,
        )
        assert user.username == "student1"
        assert user.email == "student@example.com"
        assert user.role == UserRole.STUDENT
        assert user.check_password("testpass123")

    def test_create_teacher_user(self):
        user = User.objects.create_user(
            username="teacher1",
            email="teacher@example.com",
            password="testpass123",
            role=UserRole.TEACHER,
        )
        assert user.role == UserRole.TEACHER

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="adminpass"
        )
        assert admin.is_superuser
        assert admin.is_staff
        assert admin.role == UserRole.ADMIN

    def test_email_unique(self):
        User.objects.create_user(username="test1", email="same@example.com")
        with pytest.raises(IntegrityError):
            User.objects.create_user(username="test2", email="same@example.com")
