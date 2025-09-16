from rest_framework import permissions
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwnerOrModeratorOrAdmin, CanDeleteCourseOrLesson
from materials.task import send_course_update_notification


class CourseViewSet(ModelViewSet):
    """Вьюшка  Курсов , наследующегося от Моделвиевсет (создание, удаление,
    редактирование и просмотра"""

    queryset = Course.objects.prefetch_related("lessons").all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        object = serializer.save()
        object.owner = self.request.user
        object.save()

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_permissions(self):
        if self.action == "create":
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ["update", "partial_update", "retrieve"]:
            permission_classes = [
                permissions.IsAuthenticated,
                IsOwnerOrModeratorOrAdmin,
            ]
        elif self.action == "destroy":
            permission_classes = [permissions.IsAuthenticated, CanDeleteCourseOrLesson]
        elif self.action in ["list"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_update(self, serializer):
        course = serializer.save()
        send_course_update_notification.delay(course.id)


class LessonCreateApiView(CreateAPIView):
    """Создание уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    """Отображение уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateApiView(UpdateAPIView):
    """Редактирование уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModeratorOrAdmin]


class LessonDestroyApiView(DestroyAPIView):
    """Удаление уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, CanDeleteCourseOrLesson]


class LessonRetrieveApiView(RetrieveAPIView):
    """Детальный просмотр"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrModeratorOrAdmin]


class SubscriptionAPIView(APIView):
    """Подписка на курсы"""

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")

        if not course_id:
            return Response({"error": "Не указан course_id"}, status=400)

        course = get_object_or_404(Course, id=course_id)

        subscription = Subscription.objects.filter(user_sub=user, course_sub=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user_sub=user, course_sub=course)
            message = "Подписка добавлена"

        return Response({"message": message})
