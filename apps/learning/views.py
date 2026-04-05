from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.courses.models import Exercise, Lesson, VocabularyWord
from .models import (DailyGoal, DailyStats, ExerciseResult, KnownWord,
                     LessonProgress, UserProgress)
from .serializers import (DailyGoalSerializer, ExerciseResultSerializer,
                          KnownWordSerializer, LessonProgressSerializer,
                          UserProgressSerializer)


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Студент видит только свой прогресс, учитель/админ — всех (опционально)
        user = self.request.user
        if user.role in ["teacher", "admin"]:
            return UserProgress.objects.all()
        return UserProgress.objects.filter(user=user)

    def get_object(self):
        # Для эндпоинта /my-stats/ возвращаем или создаём прогресс текущего пользователя
        obj, created = UserProgress.objects.get_or_create(user=self.request.user)
        return obj

    @action(detail=False, methods=["get"], url_path="my-stats")
    def my_stats(self, request):
        progress = self.get_object()
        serializer = self.get_serializer(progress)
        return Response(serializer.data)


class LessonProgressViewSet(viewsets.ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Только свой прогресс, если не учитель
        if self.request.user.role in ["teacher", "admin"]:
            return LessonProgress.objects.all()
        return LessonProgress.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="complete")
    def complete(self, request):
        lesson_id = request.data.get("lesson_id")
        score = request.data.get("score", 0)
        time_spent = request.data.get("time_spent", 0)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND
            )

        progress, created = LessonProgress.objects.get_or_create(
            user=request.user, lesson=lesson
        )

        if not progress.completed:
            progress.completed = True
            progress.completed_at = timezone.now()
            progress.score = score
            progress.time_spent = time_spent
            progress.attempts += 1
            progress.save()

            # Обновляем общий прогресс пользователя
            user_progress, _ = UserProgress.objects.get_or_create(user=request.user)
            user_progress.lessons_completed += 1
            user_progress.total_points += score

            # Обновляем статистику за день
            today = timezone.now().date()
            daily_stats, _ = DailyStats.objects.get_or_create(
                user=request.user, date=today
            )
            daily_stats.minutes_spent += time_spent // 60
            daily_stats.exercises_completed += 1
            daily_stats.points_earned += score
            daily_stats.save()

            user_progress.save()

        return Response(
            {"status": "completed", "progress": LessonProgressSerializer(progress).data}
        )


class ExerciseResultViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ExerciseResult.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        exercise_id = request.data.get("exercise")
        user_answer = request.data.get("user_answer")

        try:
            exercise = Exercise.objects.get(id=exercise_id)
        except Exercise.DoesNotExist:
            return Response(
                {"error": "Exercise not found"}, status=status.HTTP_404_NOT_FOUND
            )

        is_correct = (
            user_answer.strip().lower() == exercise.correct_answer.strip().lower()
        )
        points_earned = exercise.points if is_correct else 0

        result, created = ExerciseResult.objects.update_or_create(
            user=request.user,
            exercise=exercise,
            defaults={
                "user_answer": user_answer,
                "is_correct": is_correct,
                "points_earned": points_earned,
            },
        )

        if is_correct:
            user_progress, _ = UserProgress.objects.get_or_create(user=request.user)
            user_progress.total_points += points_earned
            user_progress.exercises_solved += 1
            user_progress.save()

            today = timezone.now().date()
            daily_stats, _ = DailyStats.objects.get_or_create(
                user=request.user, date=today
            )
            daily_stats.exercises_completed += 1
            daily_stats.points_earned += points_earned
            daily_stats.save()

        serializer = self.get_serializer(result)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class KnownWordViewSet(viewsets.ModelViewSet):
    serializer_class = KnownWordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return KnownWord.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"], url_path="learn")
    def learn(self, request):
        word_id = request.data.get("word_id")

        try:
            word = VocabularyWord.objects.get(id=word_id)
        except VocabularyWord.DoesNotExist:
            return Response(
                {"error": "Word not found"}, status=status.HTTP_404_NOT_FOUND
            )

        known_word, created = KnownWord.objects.get_or_create(
            user=request.user, word=word
        )

        if not known_word.mastered:
            known_word.review_count += 1
            if known_word.review_count >= 3:
                known_word.mastered = True
                user_progress, _ = UserProgress.objects.get_or_create(user=request.user)
                user_progress.words_learned += 1
                user_progress.save()
            known_word.save()

        return Response({"status": "learned", "mastered": known_word.mastered})


class DailyGoalViewSet(viewsets.ModelViewSet):
    serializer_class = DailyGoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DailyGoal.objects.filter(user=self.request.user)

    def get_object(self):
        obj, created = DailyGoal.objects.get_or_create(user=self.request.user)
        return obj
