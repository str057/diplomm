from rest_framework import serializers

from .models import Exercise, GrammarRule, Lesson, Level, Topic, VocabularyWord


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ["id", "code", "name", "description", "order"]


class TopicSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source="level.name", read_only=True)

    class Meta:
        model = Topic
        fields = ["id", "name", "icon", "level", "level_name", "order"]


class VocabularyWordSerializer(serializers.ModelSerializer):
    level_code = serializers.CharField(source="level.code", read_only=True)
    topic_names = serializers.StringRelatedField(
        source="topics", many=True, read_only=True
    )

    class Meta:
        model = VocabularyWord
        fields = [
            "id",
            "word",
            "translation",
            "transcription",
            "part_of_speech",
            "definition",
            "example",
            "example_translation",
            "image_url",
            "audio_url",
            "level",
            "level_code",
            "topics",
            "topic_names",
            "difficulty",
        ]


class GrammarRuleSerializer(serializers.ModelSerializer):
    level_code = serializers.CharField(source="level.code", read_only=True)

    class Meta:
        model = GrammarRule
        fields = [
            "id",
            "title",
            "description",
            "rule",
            "examples",
            "level",
            "level_code",
            "order",
        ]


class LessonSerializer(serializers.ModelSerializer):
    lesson_type_display = serializers.CharField(
        source="get_lesson_type_display", read_only=True
    )
    level_code = serializers.CharField(source="level.code", read_only=True)

    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "description",
            "lesson_type",
            "lesson_type_display",
            "level",
            "level_code",
            "topic",
            "content",
            "order",
            "duration_minutes",
            "is_free",
        ]


class LessonDetailSerializer(LessonSerializer):
    vocabulary_words = VocabularyWordSerializer(many=True, read_only=True)
    grammar_rules = GrammarRuleSerializer(many=True, read_only=True)

    class Meta(LessonSerializer.Meta):
        fields = LessonSerializer.Meta.fields + ["vocabulary_words", "grammar_rules"]


class ExerciseSerializer(serializers.ModelSerializer):
    exercise_type_display = serializers.CharField(
        source="get_exercise_type_display", read_only=True
    )

    class Meta:
        model = Exercise
        fields = [
            "id",
            "title",
            "exercise_type",
            "exercise_type_display",
            "question",
            "options",
            "correct_answer",
            "explanation",
            "points",
            "order",
        ]
        # correct_answer не показываем в обычном списке, только для проверки
        extra_kwargs = {"correct_answer": {"write_only": True}}
