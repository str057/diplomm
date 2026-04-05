from rest_framework import permissions, viewsets
from apps.users.permissions import IsTeacher
from .models import Exercise, GrammarRule, Lesson, Level, Topic, VocabularyWord
from .serializers import (ExerciseSerializer, GrammarRuleSerializer,
                          LessonDetailSerializer, LessonSerializer,
                          LevelSerializer, TopicSerializer,
                          VocabularyWordSerializer)


class LevelViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get("level")
        if level:
            queryset = queryset.filter(level__code=level)
        return queryset


class VocabularyWordViewSet(viewsets.ModelViewSet):
    queryset = VocabularyWord.objects.all()
    serializer_class = VocabularyWordSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get("level")
        topic = self.request.query_params.get("topic")
        difficulty = self.request.query_params.get("difficulty")
        if level:
            queryset = queryset.filter(level__code=level)
        if topic:
            queryset = queryset.filter(topics__id=topic)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset


class GrammarRuleViewSet(viewsets.ModelViewSet):
    queryset = GrammarRule.objects.all()
    serializer_class = GrammarRuleSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get("level")
        if level:
            queryset = queryset.filter(level__code=level)
        return queryset


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LessonDetailSerializer
        return LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        level = self.request.query_params.get("level")
        lesson_type = self.request.query_params.get("type")
        topic = self.request.query_params.get("topic")
        if level:
            queryset = queryset.filter(level__code=level)
        if lesson_type:
            queryset = queryset.filter(lesson_type=lesson_type)
        if topic:
            queryset = queryset.filter(topic__id=topic)
        return queryset


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsTeacher()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        queryset = super().get_queryset()
        lesson = self.request.query_params.get("lesson")
        if lesson:
            queryset = queryset.filter(lesson__id=lesson)
        return queryset
