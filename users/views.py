from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer, UserDetailSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        return UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method', )
    ordering_fields = ('date', )
