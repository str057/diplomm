from django.db import models


class Level(models.Model):
    """Уровень владения английским (CEFR)"""

    LEVEL_CHOICES = [
        ("A1", "Beginner (A1)"),
        ("A2", "Elementary (A2)"),
        ("B1", "Intermediate (B1)"),
        ("B2", "Upper Intermediate (B2)"),
        ("C1", "Advanced (C1)"),
        ("C2", "Proficient (C2)"),
    ]

    code = models.CharField(max_length=2, choices=LEVEL_CHOICES, unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Topic(models.Model):
    """Тема для изучения"""

    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome icon")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="topics")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.level.code})"


class VocabularyWord(models.Model):
    """Слово для изучения"""

    word = models.CharField(max_length=100)
    translation = models.CharField(max_length=200)
    transcription = models.CharField(max_length=100, blank=True)
    part_of_speech = models.CharField(
        max_length=50,
        blank=True,
        choices=[
            ("noun", "Существительное"),
            ("verb", "Глагол"),
            ("adjective", "Прилагательное"),
            ("adverb", "Наречие"),
            ("preposition", "Предлог"),
            ("conjunction", "Союз"),
        ],
    )
    definition = models.TextField(blank=True)
    example = models.TextField(blank=True, help_text="Пример использования")
    example_translation = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="vocabulary"
    )
    topics = models.ManyToManyField(Topic, related_name="vocabulary", blank=True)
    difficulty = models.IntegerField(
        default=1, choices=[(1, "Легкий"), (2, "Средний"), (3, "Сложный")]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Vocabulary words"
        ordering = ["word"]

    def __str__(self):
        return f"{self.word} - {self.translation}"


class GrammarRule(models.Model):
    """Грамматическое правило"""

    title = models.CharField(max_length=200)
    description = models.TextField()
    rule = models.TextField(help_text="Правило с примерами")
    examples = models.TextField(help_text="Примеры использования")
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, related_name="grammar_rules"
    )
    topics = models.ManyToManyField(Topic, related_name="grammar_rules", blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Урок английского"""

    LESSON_TYPE = [
        ("vocabulary", "Словарный запас"),
        ("grammar", "Грамматика"),
        ("listening", "Аудирование"),
        ("reading", "Чтение"),
        ("speaking", "Разговорная практика"),
        ("writing", "Письмо"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="lessons")
    topic = models.ForeignKey(
        Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name="lessons"
    )
    content = models.TextField(help_text="Основной контент урока")
    vocabulary_words = models.ManyToManyField(
        VocabularyWord, related_name="lessons", blank=True
    )
    grammar_rules = models.ManyToManyField(
        GrammarRule, related_name="lessons", blank=True
    )
    order = models.IntegerField(default=0)
    duration_minutes = models.IntegerField(default=0)
    is_free = models.BooleanField(default=False)

    class Meta:
        ordering = ["level", "order"]

    def __str__(self):
        return f"{self.title} ({self.get_lesson_type_display()})"


class Exercise(models.Model):
    """Упражнение для закрепления"""

    EXERCISE_TYPE = [
        ("multiple_choice", "Выбор правильного ответа"),
        ("fill_blank", "Заполнить пропуск"),
        ("matching", "Сопоставление"),
        ("translation", "Перевод"),
        ("listening", "Аудирование"),
        ("writing", "Написание"),
    ]

    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="exercises"
    )
    title = models.CharField(max_length=200)
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE)
    question = models.TextField()
    correct_answer = models.TextField()
    options = models.JSONField(
        default=list, blank=True, help_text="Для multiple_choice: список вариантов"
    )
    explanation = models.TextField(
        blank=True, help_text="Объяснение правильного ответа"
    )
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"
