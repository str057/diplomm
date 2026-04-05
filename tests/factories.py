import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Faker

from apps.courses.models import (Exercise, GrammarRule, Lesson, Level, Topic,
                                 VocabularyWord)
from apps.learning.models import (DailyGoal, DailyStats, ExerciseResult,
                                  KnownWord, LessonProgress, UserProgress)

fake = Faker()
User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = (
            True  # предотвращает лишнее сохранение после пост-генерации
        )

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "testpass123")
    role = "student"


class AdminFactory(UserFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    role = "admin"
    is_staff = True
    is_superuser = True


class TeacherFactory(UserFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    role = "teacher"


class LevelFactory(DjangoModelFactory):
    class Meta:
        model = Level

    code = factory.Iterator(["A1", "A2", "B1", "B2", "C1"])
    name = factory.LazyAttribute(lambda o: f"Level {o.code}")
    order = factory.Sequence(lambda n: n)


class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = factory.Sequence(lambda n: f"Topic {n}")
    level = factory.SubFactory(LevelFactory)
    order = factory.Sequence(lambda n: n)


class VocabularyWordFactory(DjangoModelFactory):
    class Meta:
        model = VocabularyWord

    word = factory.Sequence(lambda n: f"word{n}")
    translation = factory.Sequence(lambda n: f"перевод{n}")
    level = factory.SubFactory(LevelFactory)
    difficulty = 1


class GrammarRuleFactory(DjangoModelFactory):
    class Meta:
        model = GrammarRule

    title = factory.Sequence(lambda n: f"Rule {n}")
    description = "Test description"
    rule = "Test rule"
    examples = "Example1\nExample2"
    level = factory.SubFactory(LevelFactory)
    order = factory.Sequence(lambda n: n)


class LessonFactory(DjangoModelFactory):
    class Meta:
        model = Lesson

    title = factory.Sequence(lambda n: f"Lesson {n}")
    lesson_type = "vocabulary"
    level = factory.SubFactory(LevelFactory)
    content = "Lesson content"
    order = factory.Sequence(lambda n: n)
    duration_minutes = 30


class ExerciseFactory(DjangoModelFactory):
    class Meta:
        model = Exercise

    lesson = factory.SubFactory(LessonFactory)
    title = factory.Sequence(lambda n: f"Exercise {n}")
    exercise_type = "translation"
    question = "Question"
    correct_answer = "answer"
    points = 10
    order = factory.Sequence(lambda n: n)


class UserProgressFactory(DjangoModelFactory):
    class Meta:
        model = UserProgress

    user = factory.SubFactory(UserFactory)
    current_level = factory.SubFactory(LevelFactory)
    total_points = 0
    lessons_completed = 0
    streak_days = 0


class LessonProgressFactory(DjangoModelFactory):
    class Meta:
        model = LessonProgress

    user = factory.SubFactory(UserFactory)
    lesson = factory.SubFactory(LessonFactory)
    completed = False


class ExerciseResultFactory(DjangoModelFactory):
    class Meta:
        model = ExerciseResult

    user = factory.SubFactory(UserFactory)
    exercise = factory.SubFactory(ExerciseFactory)
    user_answer = "answer"
    is_correct = True
    points_earned = 10


class KnownWordFactory(DjangoModelFactory):
    class Meta:
        model = KnownWord

    user = factory.SubFactory(UserFactory)
    word = factory.SubFactory(VocabularyWordFactory)
    mastered = False


class DailyGoalFactory(DjangoModelFactory):
    class Meta:
        model = DailyGoal

    user = factory.SubFactory(UserFactory)
    minutes_per_day = 30
    words_per_day = 10
    exercises_per_day = 5


class DailyStatsFactory(DjangoModelFactory):
    class Meta:
        model = DailyStats

    user = factory.SubFactory(UserFactory)
    minutes_spent = 15
    words_learned = 5
    exercises_completed = 3
    points_earned = 30
