from celery import shared_task
from config import settings
from lms.models import Course, Subscription
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_notification(course_id, user_ids):
    logger.info(f"Получена задача для курса {course_id} и пользователей {user_ids}")
    for user_id in user_ids:
        try:
            course = Course.objects.get(id=course_id)
            user = Subscription.objects.get(user_id=user_id, course_id=course_id).user

            subject = f'Обновление курса: {course.title}'
            message = f'В курс {course.title} были внесены изменения.\n' \
                      f'Подробности: {settings.FRONTEND_URL}/course/{course.id}'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [user.email]

            send_mail(
                subject,
                message,
                from_email,
                recipient_list,
                fail_silently=False
            )
            logger.info(f'Уведомление отправлено пользователю {user.email}')
        except ObjectDoesNotExist as e:
            logger.error(f'Ошибка при отправке уведомления пользователю {user.email}: {str(e)}')
