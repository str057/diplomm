from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import User
from .permissions import IsOwnerOrTeacher, IsTeacher
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":
            # Регистрация доступна всем
            return [permissions.AllowAny()]
        elif self.action in ["list", "retrieve"]:
            # Просмотр списка и деталей только для авторизованных
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            # Изменение/удаление только владельцу или учителю
            return [IsOwnerOrTeacher()]
        elif self.action == "change_role":
            # Смена роли только учителю/админу
            return [IsTeacher()]
        return super().get_permissions()

    @action(
        detail=True, methods=["post"], url_path="change-role", url_name="change-role"
    )
    def change_role(self, request, pk=None):
        user = self.get_object()
        new_role = request.data.get("role")
        # Используем get_role_display или choices из модели
        valid_roles = [choice[0] for choice in User._meta.get_field("role").choices]
        if new_role not in valid_roles:
            return Response(
                {"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST
            )
        if request.user.role == "teacher" and new_role == "admin":
            return Response(
                {"error": "Teacher cannot assign admin role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        user.role = new_role
        user.save()
        return Response({"status": "role updated", "role": user.role})

    @action(detail=False, methods=["get"], url_path="me", url_name="me")
    def me(self, request):
        """Возвращает профиль текущего авторизованного пользователя."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "courses": "/api/courses/",
            "learning": "/api/learning/",
            "docs": "/api/docs/swagger/",
            "redoc": "/api/docs/redoc/",
        }
    )
