from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_video_urls


class LessonSerializer(ModelSerializer):
    """Класс сериализатора  для вьюсета Уроков для отображения параметров"""

    class Meta:
        model = Lesson
        fields = "__all__"
        extra_kwargs = {
            'video_url': {'validators': [validate_video_urls]}
        }


class CourseSerializer(ModelSerializer):
    """Класс сериализатора  для вьюсета Курса для отображения параметров,
    так же добавлено новое поле и оформление подписки"""

    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, instance):
        return instance.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user_sub=request.user,
                course_sub=obj
            ).exists()
        return False
