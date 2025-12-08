from django.contrib.auth.models import AbstractUser
from django.db import models
from lms.models import Course, Lesson


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Введите электронную почту",
    )
    phone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="Номер телефона",
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Город",
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Пользователь",
        related_name="payments",
    )
    date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата оплаты"
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный курс",
        related_name="payments",
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Оплаченный урок",
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Сумма оплаты",
    )
    payment_method = models.CharField(
        max_length=20,
        choices=(("cash", "Наличные"), ("transfer", "Перевод на счет")),
        null=True,
        blank=True,
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID сессии'
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name='Ссылка на оплату'
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return self.user, self.amount
