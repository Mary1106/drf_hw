from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import UserCreateAPIView, PaymentCreateAPIView

app_name = UsersConfig.name

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('pay/course/<int:course_id>/', PaymentCreateAPIView.as_view(), name='pay_course')
]
