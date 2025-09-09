import stripe

from config import settings
from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

class StripeService:
    """ Сервис для работы с Stripe: создание продукта, цены и оплаты """

    @staticmethod
    def create_product_and_price(course):
        """
        Создаёт продукт и цену в Stripe для курса
        """
        try:
            product = stripe.Product.create(
                name=course.name,
                description=course.description or "",
                metadata={"course_id": course.id}
            )


            price = stripe.Price.create(
                product=product.id,
                unit_amount=2000,
                currency='usd',
                metadata={"course_id": course.id}
            )

            course.stripe_product_id = product.id
            course.stripe_price_id = price.id
            course.save()

            return {
                "success": True,
                "product_id": product.id,
                "price_id": price.id
            }

        except stripe.StripeError as e:
            return {
                "success": False,
                "error": f"Ошибка Stripe: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Неизвестная ошибка: {str(e)}"
            }

    @staticmethod
    def create_checkout_session(course, user):
        """
        Создаёт сессию оплаты и возвращает ссылку
        """
        if not course.stripe_price_id:
            return {
                "success": False,
                "error": "Для этого курса не настроена цена в Stripe"
            }

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': course.stripe_price_id,
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.STRIPE_SUCCESS_URL,
                cancel_url=settings.STRIPE_CANCEL_URL,
                metadata={
                    "course_id": course.id,
                    "user_id": user.id
                }
            )

            return {
                "success": True,
                "url": session.url
            }

        except stripe.StripeError as e:
            return {
                "success": False,
                "error": f"Ошибка Stripe: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Неизвестная ошибка: {str(e)}"
            }