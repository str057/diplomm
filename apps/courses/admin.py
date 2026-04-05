from django.contrib import admin

from .models import Exercise, GrammarRule, Lesson, Level, Topic, VocabularyWord


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "order")
    list_editable = ("order",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "level", "order")
    list_filter = ("level",)
    list_editable = ("order",)


@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display = ("word", "translation", "part_of_speech", "level", "difficulty")
    list_filter = ("level", "part_of_speech", "difficulty")
    search_fields = ("word", "translation")
    filter_horizontal = ("topics",)


@admin.register(GrammarRule)
class GrammarRuleAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "order")
    list_filter = ("level",)
    filter_horizontal = ("topics",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson_type", "level", "duration_minutes", "is_free")
    list_filter = ("lesson_type", "level", "is_free")
    filter_horizontal = ("vocabulary_words", "grammar_rules")


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("title", "lesson", "exercise_type", "points", "order")
    list_filter = ("exercise_type",)
