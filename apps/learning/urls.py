from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DailyGoalViewSet, ExerciseResultViewSet, KnownWordViewSet,
                    LessonProgressViewSet, UserProgressViewSet)

router = DefaultRouter()
router.register(r"progress", UserProgressViewSet, basename="user-progress")
router.register(r"lesson-progress", LessonProgressViewSet, basename="lesson-progress")
router.register(r"exercise-results", ExerciseResultViewSet, basename="exercise-result")
router.register(r"known-words", KnownWordViewSet, basename="known-word")
router.register(r"daily-goal", DailyGoalViewSet, basename="daily-goal")

urlpatterns = [
    path("", include(router.urls)),
]
