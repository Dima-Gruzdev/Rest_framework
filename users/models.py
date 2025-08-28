from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.CharField(
        max_length=15,
        verbose_name="Телефон",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите свое фото",
    )
    city = models.CharField(
        max_length=30,
        verbose_name="Страна",
        blank=True,
        null=True,
        help_text="Введите город в котором проживаете",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name="user", verbose_name="Пользователь"
    )
    data_pay = models.DateTimeField(auto_now=True, verbose_name='Дата оплаты')
    data_pay_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Дата оплаты курса'
    )
    data_pay_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дата оплаты урока"
    )
    sum_pay = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты')
    method_pay = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'{self.user} - {self.data_pay} {self.sum_pay} {self.method_pay}'
