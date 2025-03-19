from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import User, Payment


class Command(BaseCommand):
    help = "Add payments to the DB"

    def handle(self, *args, **kwargs):
        # Удаление платежей из БД перед добавлением тестовых:
        Payment.objects.all().delete()

        user, _ = User.objects.get_or_create(email='one@mail.com')
        course, _ = Course.objects.get_or_create(id='1')
        lesson, _ = Lesson.objects.get_or_create(id='1')

        payments = [
            {
                "user": user,
                "date": "2025-03-19",
                "paid_course": course,
                "paid_lesson": None,
                "amount": "100000",
                "payment_method": "transfer",
            },
            {
                "user": user,
                "date": "2025-03-19",
                "paid_course": None,
                "paid_lesson": lesson,
                "amount": "10000",
                "payment_method": "transfer",
            },
        ]

        for payment in payments:
            payment, created = Payment.objects.get_or_create(**payment)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Платеж добавлен. Пользователь: {payment.user}, курс/урок: {payment.paid_course}/{payment.paid_lesson}."
                    )
                )
            else:
                self.stdout.write(self.style.WARNING(f"Платеж уже существует"))
