from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users import views
from users.apps import UsersConfig
from users.views import UserCreateAPIView

router = DefaultRouter()
router.register(r"payments", views.PaymentViewSet)

app_name = UsersConfig.name

urlpatterns = [
    path("register", UserCreateAPIView.as_view(), name="register"),
    path("api/", include(router.urls)),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
]
