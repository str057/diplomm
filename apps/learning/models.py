from django.conf import settings
from django.db import models

from apps.courses.models import Exercise, Lesson, VocabularyWord


class UserProgress(models.Model):
    """Общий прогресс пользователя"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="english_progress",
    )
    current_level = models.ForeignKey(
        "courses.Level",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    total_points = models.IntegerField(default=0)
    lessons_completed = models.IntegerField(default=0)
    exercises_solved = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    streak_days = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Progress: {self.user.username}"


class LessonProgress(models.Model):
    """Прогресс по уроку"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="lesson_progress",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="user_progress"
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0, help_text="Процент правильных ответов")
    time_spent = models.IntegerField(default=0, help_text="Время в секундах")
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ["user", "lesson"]

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class ExerciseResult(models.Model):
    """Результат выполнения упражнения"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="results"
    )
    user_answer = models.TextField()
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "exercise"]

    def __str__(self):
        status = '✓' if self.is_correct else '✗'
        return f"{self.user.username} - {self.exercise.title}: {status}"


class KnownWord(models.Model):
    """Слова, которые пользователь уже выучил"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="known_words"
    )
    word = models.ForeignKey(
        VocabularyWord,
        on_delete=models.CASCADE
    )
    mastered = models.BooleanField(default=False, help_text="Полностью освоено")
    review_count = models.IntegerField(default=0)
    last_reviewed = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "word"]

    def __str__(self):
        return f"{self.user.username} knows {self.word.word}"


class DailyGoal(models.Model):
    """Ежедневная цель пользователя"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_goal"
    )
    minutes_per_day = models.IntegerField(default=30, help_text="Минут в день")
    words_per_day = models.IntegerField(default=10, help_text="Слов в день")
    exercises_per_day = models.IntegerField(default=5, help_text="Упражнений в день")

    def __str__(self):
        return f"Goals for {self.user.username}"


class DailyStats(models.Model):
    """Статистика за день"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="daily_stats"
    )
    date = models.DateField(auto_now_add=True)
    minutes_spent = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    exercises_completed = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)

    class Meta:
        unique_together = ["user", "date"]
        ordering = ["-date"]

    def __str__(self):
        return f"{self.user.username} - {self.date}"
