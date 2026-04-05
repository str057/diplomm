from rest_framework import serializers

from .models import (DailyGoal, DailyStats, ExerciseResult, KnownWord,
                     LessonProgress, UserProgress)


class UserProgressSerializer(serializers.ModelSerializer):
    current_level_code = serializers.CharField(
        source="current_level.code", read_only=True
    )

    class Meta:
        model = UserProgress
        fields = [
            "id",
            "current_level",
            "current_level_code",
            "total_points",
            "lessons_completed",
            "exercises_solved",
            "words_learned",
            "streak_days",
            "last_activity",
        ]
        read_only_fields = [
            "total_points",
            "lessons_completed",
            "exercises_solved",
            "words_learned",
            "streak_days",
        ]


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    lesson_type = serializers.CharField(source="lesson.lesson_type", read_only=True)

    class Meta:
        model = LessonProgress
        fields = [
            "id",
            "lesson",
            "lesson_title",
            "lesson_type",
            "completed",
            "score",
            "time_spent",
            "attempts",
        ]


class ExerciseResultSerializer(serializers.ModelSerializer):
    exercise_title = serializers.CharField(source="exercise.title", read_only=True)

    class Meta:
        model = ExerciseResult
        fields = [
            "id",
            "exercise",
            "exercise_title",
            "user_answer",
            "is_correct",
            "points_earned",
            "completed_at",
        ]


class KnownWordSerializer(serializers.ModelSerializer):
    word_text = serializers.CharField(source="word.word", read_only=True)
    translation = serializers.CharField(source="word.translation", read_only=True)

    class Meta:
        model = KnownWord
        fields = [
            "id",
            "word",
            "word_text",
            "translation",
            "mastered",
            "review_count",
            "last_reviewed",
        ]


class DailyGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyGoal
        fields = ["id", "minutes_per_day", "words_per_day", "exercises_per_day"]


class DailyStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStats
        fields = [
            "id",
            "date",
            "minutes_spent",
            "words_learned",
            "exercises_completed",
            "points_earned",
        ]
