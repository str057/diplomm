import pytest

from apps.courses.models import (Exercise, GrammarRule, Lesson, Level, Topic,
                                 VocabularyWord)
from tests.factories import (LessonFactory, LevelFactory, TopicFactory,
                             VocabularyWordFactory)

pytestmark = pytest.mark.django_db


class TestLevel:
    def test_create_level(self):
        level = Level.objects.create(code="B1", name="Intermediate", order=3)
        assert level.code == "B1"
        assert str(level) == "B1 - Intermediate"

    def test_level_ordering(self):
        Level.objects.create(code="A2", name="Elementary", order=2)
        Level.objects.create(code="A1", name="Beginner", order=1)
        levels = list(Level.objects.all())
        assert levels[0].code == "A1"
        assert levels[1].code == "A2"


class TestTopic:
    def test_create_topic(self):
        level = LevelFactory()
        topic = Topic.objects.create(name="Grammar", level=level, order=1)
        assert topic.name == "Grammar"
        assert topic.level == level


class TestVocabularyWord:
    def test_create_word(self):
        level = LevelFactory()
        word = VocabularyWord.objects.create(
            word="hello", translation="привет", level=level, difficulty=1
        )
        assert word.word == "hello"
        assert str(word) == "hello - привет"

    def test_word_topics(self):
        level = LevelFactory()
        topic = TopicFactory(level=level)
        word = VocabularyWordFactory(level=level)
        word.topics.add(topic)
        assert topic in word.topics.all()


class TestGrammarRule:
    def test_create_rule(self):
        level = LevelFactory()
        rule = GrammarRule.objects.create(
            title="Present Simple",
            description="Tense",
            rule="Use for facts",
            examples="I work",
            level=level,
            order=1,
        )
        assert rule.title == "Present Simple"


class TestLesson:
    def test_create_lesson(self):
        level = LevelFactory()
        lesson = Lesson.objects.create(
            title="My Lesson",
            lesson_type="vocabulary",
            level=level,
            content="Content",
            order=1,
        )
        assert lesson.title == "My Lesson"

    def test_lesson_ordering(self):
        level = LevelFactory()
        Lesson.objects.create(
            title="Lesson 2", lesson_type="vocabulary", level=level, content="", order=2
        )
        Lesson.objects.create(
            title="Lesson 1", lesson_type="vocabulary", level=level, content="", order=1
        )
        lessons = list(Lesson.objects.filter(level=level))
        assert lessons[0].order == 1
        assert lessons[1].order == 2


class TestExercise:
    def test_create_exercise(self):
        lesson = LessonFactory()
        exercise = Exercise.objects.create(
            lesson=lesson,
            title="Ex1",
            exercise_type="translation",
            question="Hello",
            correct_answer="Привет",
            points=5,
            order=1,
        )
        assert exercise.title == "Ex1"
        assert exercise.points == 5
