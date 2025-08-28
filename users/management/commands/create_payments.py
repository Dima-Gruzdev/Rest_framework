from django.core.management import BaseCommand

from config import settings
from materials.models import Course, Lesson
from users.models import Payments


class Command(BaseCommand):
    help = 'Создаёт тестовые платежи'

    def handle(self, *args, **options):
        user1 = settings.AUTH_USER_MODEL.objects.get(email='user1@example.com')  # или используйте pk
        user2 = settings.AUTH_USER_MODEL.objects.get(email='user2@example.com')

        course = Course.objects.first()
        lesson = Lesson.objects.first()

        if not course or not lesson:
            self.stdout.write(self.style.ERROR('Сначала создайте курсы и уроки!'))
            return

        Payments.objects.create(
            user=user1,
            paid_course=course,
            amount=15000.00,
            payment_method='transfer'
        )

        Payments.objects.create(
            user=user2,
            paid_lesson=lesson,
            amount=2500.50,
            payment_method='cash'
        )

        self.stdout.write(
            self.style.SUCCESS('Тестовые платежи успешно созданы!')
        )