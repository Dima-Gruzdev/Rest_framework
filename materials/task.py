from celery import shared_task
from django.core.mail import send_mail
from .models import Subscription, Course
from django.conf import settings


@shared_task
def send_course_update_notification(course_id):
    """ Отправляет письма на почту всем подписчикам курса при его обновлении """
    try:
        course = Course.objects.get(id=course_id)
        subscribers = Subscription.objects.filter(course_sub=course).select_related('user_sub')

        if not subscribers.exists():
            return f"Нет подписчиков для курса '{course.name}'"

        recipient_list = [sub.user_sub.email for sub in subscribers]

        subject = f"Обновление курса: {course.name}"
        message = (
            f"Здравствуйте!\n\n"
            f"Курс '{course.name}' был обновлён.\n"
            f"Описание: {course.description or 'Без описания'}\n\n"
            f"Перейдите в приложение, чтобы посмотреть изменения."
        )
        from_email = settings.DEFAULT_FROM_EMAIL

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

        return f"Успешно отправлено {len(recipient_list)} письма(м)"

    except Course.DoesNotExist:
        return f"Ошибка: курс с ID={course_id} не найден"
    except Exception as e:
        return f"Ошибка при отправке: {str(e)}"
