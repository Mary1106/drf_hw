from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User
import logging


logger = logging.getLogger(__name__)


@shared_task
def block_inactive_users():
    # Задаем период не-активности
    inactive_period = timezone.now() - timedelta(days=30)
    # Получаем пользователей, которые не заходили более заданного периода
    inactive_users = User.objects.filter(
        last_login__lt=inactive_period,
        is_active=True
    )

    # Блокируем пользователей
    for user in inactive_users:
        user.is_active = False
        user.save()
        logger.info(f"Заблокирован пользователь: {user.username}")
