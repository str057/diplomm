import pytest
from rest_framework.test import APIRequestFactory

from apps.users.models import UserRole
from apps.users.permissions import IsAdmin, IsOwnerOrTeacher, IsTeacher
from tests.factories import AdminFactory, TeacherFactory, UserFactory

pytestmark = pytest.mark.django_db


class TestIsAdmin:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsAdmin()

    def test_admin_has_permission(self):
        user = AdminFactory()
        request = self.factory.get("/")
        request.user = user
        assert self.permission.has_permission(request, None) is True

    def test_teacher_no_permission(self):
        user = TeacherFactory()
        request = self.factory.get("/")
        request.user = user
        assert self.permission.has_permission(request, None) is False


class TestIsTeacher:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsTeacher()

    def test_teacher_has_permission(self):
        user = TeacherFactory()
        request = self.factory.get("/")
        request.user = user
        assert self.permission.has_permission(request, None) is True

    def test_student_no_permission(self):
        user = UserFactory(role=UserRole.STUDENT)
        request = self.factory.get("/")
        request.user = user
        assert self.permission.has_permission(request, None) is False


class TestIsOwnerOrTeacher:
    def setup_method(self):
        self.factory = APIRequestFactory()
        self.permission = IsOwnerOrTeacher()

    def test_owner_has_permission(self):
        user = UserFactory()
        obj = type("Obj", (), {"user": user})()
        request = self.factory.get("/")
        request.user = user
        assert self.permission.has_object_permission(request, None, obj) is True

    def test_teacher_has_permission(self):
        teacher = TeacherFactory()
        obj = type("Obj", (), {"user": UserFactory()})()
        request = self.factory.get("/")
        request.user = teacher
        assert self.permission.has_object_permission(request, None, obj) is True

    def test_other_student_no_permission(self):
        owner = UserFactory()
        other = UserFactory(role=UserRole.STUDENT)
        obj = type("Obj", (), {"user": owner})()
        request = self.factory.get("/")
        request.user = other
        assert self.permission.has_object_permission(request, None, obj) is False
