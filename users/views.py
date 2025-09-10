from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
)

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser

from config import settings
from users.filters import PaymentFilter
from users.models import Payments, User
from users.permissions import IsOwnerOrAdmin
from users.serializers import PaymentSerializer, UserSerializer
from users.services import StripeService


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrAdmin]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
    ]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "amount"]
    ordering = ["-payment_date"]

    def get_queryset(self):
        return Payments.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        pay_object = payment.course or payment.lesson
        if not pay_object:
            raise ValidationError("Укажите курс или урок")

        product_result = StripeService.create_product(pay_object)
        if not product_result["success"]:
            raise ValidationError(product_result["error"])

        price_result = StripeService.create_price(
            product_result["product"].id, float(payment.sum_pay)
        )
        if not price_result["success"]:
            raise ValidationError(price_result["error"])

        session_result = StripeService.create_checkout_session(
            price_result["price"].id,
            settings.STRIPE_SUCCESS_URL,
            settings.STRIPE_CANCEL_URL,
            {
                "payment_id": payment.id,
                "user_id": payment.user.id,
                "course_id": payment.course.id if payment.course else "",
                "lesson_id": payment.lesson.id if payment.lesson else "",
            },
        )
        if not session_result["success"]:
            raise ValidationError(session_result["error"])

        payment.payment_link = session_result["url"]
        payment.stripe_session_id = session_result["session_id"]
        payment.save()
