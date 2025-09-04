from rest_framework import permissions, filters

from lms.models import Course
from users.models import User, Payment
from lms.models import Course, Lesson
from users.serializers import UserSerializer, PaymentSerializer, UserDetailSerializer
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView, get_object_or_404
)
from users.services import create_stripe_price, create_stripe_session, create_stripe_product
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentCreateAPIView(APIView):
    serializer_class = PaymentSerializer

    def post(self, request, content_type, content_id):
        try:
            if content_type == 'lesson':
                content = get_object_or_404(Lesson, id=content_id)
                paid_lesson = content
                paid_course = None
            elif content_type == 'course':
                content = get_object_or_404(Course, id=content_id)
                paid_lesson = None
                paid_course = content
            else:
                return Response({'error': 'Неверный тип контента'}, status=status.HTTP_400_BAD_REQUEST)

            # Проверяем, создан ли уже продукт в Stripe
            if not content.stripe_product_id:
                stripe_product_id = create_stripe_product(content)
                if not stripe_product_id:
                    return Response({'error': 'Ошибка создания продукта в Stripe'},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            stripe_price = create_stripe_price(content)
            if not stripe_price:
                return Response({'error': 'Ошибка создания цены в Stripe'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            session_id, payment_link = create_stripe_session(stripe_price.id)
            if not session_id or not payment_link:
                return Response({'error': 'Ошибка создания сессии оплаты'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            payment = Payment.objects.create(
                user=request.user,
                paid_lesson=paid_lesson,
                paid_course=paid_course,
                amount=content.price,
                session_id=session_id,
                link=payment_link,
                payment_method='card'
            )

            serializer = self.serializer_class(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
