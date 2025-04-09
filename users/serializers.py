from rest_framework.serializers import ModelSerializer

from lms.serializers import CourseSerializer
from users.models import User, Payment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['user', 'date', 'paid_course', 'paid_lesson', 'amount', 'payment_method', 'session_id', 'link', 'course']


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'payments']

