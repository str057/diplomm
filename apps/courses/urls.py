from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (ExerciseViewSet, GrammarRuleViewSet, LessonViewSet,
                    LevelViewSet, TopicViewSet, VocabularyWordViewSet)

router = DefaultRouter()
router.register(r"levels", LevelViewSet)
router.register(r"topics", TopicViewSet)
router.register(r"vocabulary", VocabularyWordViewSet)
router.register(r"grammar", GrammarRuleViewSet)
router.register(r"lessons", LessonViewSet)
router.register(r"exercises", ExerciseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
