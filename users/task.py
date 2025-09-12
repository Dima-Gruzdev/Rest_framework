from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


User = get_user_model()


@shared_task
def deactivate_inactive_users():
    """ Функция проверяет и  блокирует пользователей, которые не заходили более 30 дней."""

    cutoff_date = timezone.now() - timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=cutoff_date,
        is_active=True
    )

    count = inactive_users.count()
    if count > 0:
        inactive_users.update(is_active=False)
        print(f" Не активно {count} пользователей (не заходили с {cutoff_date.strftime('%Y-%m-%d')})")
    else:
        print("Нет неактивных пользователей для блокировки")

    return f"Обработано: {count} пользователей"
