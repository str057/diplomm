from django.contrib import admin

from .models import (DailyGoal, DailyStats, ExerciseResult, KnownWord,
                     LessonProgress, UserProgress)


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "current_level",
        "total_points",
        "lessons_completed",
        "streak_days",
    )
    list_filter = ("current_level",)
    search_fields = ("user__username",)


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "completed", "score", "time_spent")
    list_filter = ("completed", "lesson__lesson_type")
    search_fields = ("user__username", "lesson__title")


@admin.register(ExerciseResult)
class ExerciseResultAdmin(admin.ModelAdmin):
    list_display = ("user", "exercise", "is_correct", "points_earned", "completed_at")
    list_filter = ("is_correct",)
    search_fields = ("user__username", "exercise__title")


@admin.register(KnownWord)
class KnownWordAdmin(admin.ModelAdmin):
    list_display = ("user", "word", "mastered", "review_count", "last_reviewed")
    list_filter = ("mastered",)
    search_fields = ("user__username", "word__word")


@admin.register(DailyGoal)
class DailyGoalAdmin(admin.ModelAdmin):
    list_display = ("user", "minutes_per_day", "words_per_day", "exercises_per_day")
    search_fields = ("user__username",)


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "minutes_spent",
        "words_learned",
        "exercises_completed",
    )
    list_filter = ("date",)
    search_fields = ("user__username",)
