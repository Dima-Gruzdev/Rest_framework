import os
from celery import Celery
from celery.schedules import crontab
from users.task import deactivate_inactive_users

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Пример другой задачи
    # sender.add_periodic_task(crontab(minute='*/30'), send_test_email.s())

    # Задача: проверять неактивных пользователей каждый день в 2:00
    sender.add_periodic_task(
        crontab(hour=2, minute=0),  # Каждый день в 02:00
        deactivate_inactive_users.s(),
        name='Ежедневная деактивация неактивных пользователей'
    )