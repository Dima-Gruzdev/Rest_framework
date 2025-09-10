from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course
from users.models import User

User = get_user_model()


class LessonTestCase(APITestCase):
    """Класс тестирования работоспособности уроков"""

    def setUp(self):
        self.user = User.objects.create_user(email="user@test.com", password="test123")

        self.admin = User.objects.create_superuser(
            email="admin@test.com", password="testpass123"
        )

        self.course = Course.objects.create(
            name="Тестовый курс", description="Описание курса", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            description="Описание",
            video_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            course=self.course,
            owner=self.user,
        )

        self.lesson_list_url = "/materials/lesson/"
        self.lesson_create_url = "/materials/lesson/create/"
        self.lesson_detail_url = f"/materials/lesson/{self.lesson.id}/"
        self.lesson_update_url = f"/materials/lesson/{self.lesson.id}/update/"
        self.lesson_delete_url = f"/materials/lesson/{self.lesson.id}/delete/"
        self.subscribe_url = "/materials/subscribe/"
        self.courses_url = "/materials/courses/"

    def test_list_lessons(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Тестовый урок")

    def test_retrieve_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Тестовый урок")

    def test_update_lesson_by_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "Обновлённый урок"}
        response = self.client.patch(self.lesson_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновлённый урок")

    def test_create_lesson_by_owner(self):
        admin = User.objects.create_superuser(
            email="admin1@test.com", password="testpass123"
        )
        self.client.force_authenticate(user=admin)

        data = {
            "name": "Новый урок",
            "description": "Описание",
            "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "course": self.course.id,
            "owner": self.user.id,
        }

        response = self.client.post(self.lesson_create_url, data, format="json")
        if response.status_code != 201:
            print("Status code:", response.status_code)
            print("Response ", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_delete_lesson_by_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_subscribe_unsubscribe(self):
        self.client.force_authenticate(user=self.user)
        data = {"course_id": self.course.id}
        response = self.client.post(self.subscribe_url, data, format="json")
        self.assertEqual(response.data["message"], "Подписка добавлена")
        response = self.client.post(self.subscribe_url, data, format="json")
        self.assertEqual(response.data["message"], "Подписка удалена")
