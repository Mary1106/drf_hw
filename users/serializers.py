from rest_framework.serializers import ModelSerializer

from users.models import User, Payment


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['email', 'phone', 'city', 'avatar', 'payments']
