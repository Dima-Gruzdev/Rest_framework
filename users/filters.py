from users.models import Payments
import django_filters


class PaymentFilter(django_filters.FilterSet):
    payment_method = django_filters.ChoiceFilter(
        choices=Payments.PAYMENT_METHOD_CHOICES
    )

    paid_course = django_filters.NumberFilter(
        field_name="paid_course", lookup_expr="exact"
    )

    paid_lesson = django_filters.NumberFilter(
        field_name="paid_lesson", lookup_expr="exact"
    )

    amount_min = django_filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount_max = django_filters.NumberFilter(field_name="amount", lookup_expr="lte")

    class Meta:
        model = Payments
        fields = [
            "payment_method",
            "paid_course",
            "paid_lesson",
            "amount_min",
            "amount_max",
        ]
