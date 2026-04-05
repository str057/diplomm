from datetime import date

import pytest

from apps.learning.models import (DailyGoal, DailyStats, ExerciseResult,
                                  KnownWord, LessonProgress, UserProgress)
from tests.factories import (ExerciseFactory, LessonFactory, LevelFactory,
                             UserFactory, VocabularyWordFactory)

pytestmark = pytest.mark.django_db


class TestUserProgress:
    def test_create_progress(self):
        user = UserFactory()
        level = LevelFactory()
        progress = UserProgress.objects.create(user=user, current_level=level)
        assert progress.user == user
        assert progress.current_level == level
        assert progress.total_points == 0


class TestLessonProgress:
    def test_lesson_progress_creation(self):
        user = UserFactory()
        lesson = LessonFactory()
        progress = LessonProgress.objects.create(user=user, lesson=lesson)
        assert progress.user == user
        assert progress.lesson == lesson
        assert not progress.completed


class TestExerciseResult:
    def test_exercise_result_creation(self):
        user = UserFactory()
        exercise = ExerciseFactory()
        result = ExerciseResult.objects.create(
            user=user,
            exercise=exercise,
            user_answer="correct",
            is_correct=True,
            points_earned=10,
        )
        assert result.is_correct
        assert result.points_earned == 10


class TestKnownWord:
    def test_known_word_creation(self):
        user = UserFactory()
        word = VocabularyWordFactory()
        known = KnownWord.objects.create(user=user, word=word)
        assert known.user == user
        assert not known.mastered


class TestDailyGoal:
    def test_daily_goal_creation(self):
        user = UserFactory()
        goal = DailyGoal.objects.create(user=user, minutes_per_day=30)
        assert goal.minutes_per_day == 30


class TestDailyStats:
    def test_daily_stats_creation(self):
        user = UserFactory()
        stats = DailyStats.objects.create(
            user=user, date=date.today(), minutes_spent=15, words_learned=5
        )
        assert stats.minutes_spent == 15
