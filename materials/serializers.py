from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = LessonSerializer(source="lessons", many=True, read_only=True)

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lesson(self, instance):
        return instance.lessons.count()
