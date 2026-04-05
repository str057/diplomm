import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from apps.users.models import UserRole
from tests.factories import TeacherFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestUserAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_register_user(self):
        url = "/api/v1/users/"
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
        }
        response = self.client.post(url, data)
        assert response.status_code == 201
        assert response.data["username"] == "newuser"

    def test_get_users_unauthenticated(self):
        url = "/api/v1/users/"
        response = self.client.get(url)
        assert response.status_code == 401

    def test_get_users_authenticated(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = "/api/v1/users/"
        response = self.client.get(url)
        assert response.status_code == 200

    def test_me_endpoint(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        url = "/api/v1/users/me/"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["username"] == user.username

    def test_change_role_by_teacher(self):
        teacher = TeacherFactory()
        student = UserFactory(role=UserRole.STUDENT)
        self.client.force_authenticate(user=teacher)
        url = reverse("user-change-role", kwargs={"pk": student.pk})
        response = self.client.post(url, {"role": "teacher"})
        assert response.status_code == 200
        student.refresh_from_db()
        assert student.role == UserRole.TEACHER

    def test_change_role_by_student_forbidden(self):
        student = UserFactory(role=UserRole.STUDENT)
        other = UserFactory(role=UserRole.STUDENT)
        self.client.force_authenticate(user=student)
        url = reverse("user-change-role", kwargs={"pk": other.pk})
        response = self.client.post(url, {"role": "teacher"})
        assert response.status_code == 403

    def test_token_obtain(self):
        user = UserFactory()
        user.set_password("testpass123")
        user.save()
        url = "/api/v1/token/"
        response = self.client.post(
            url, {"username": user.username, "password": "testpass123"}
        )
        assert response.status_code == 200
        assert "access" in response.data
