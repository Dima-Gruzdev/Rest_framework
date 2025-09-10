import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


class StripeService:

    @staticmethod
    def create_product(course):
        """Создаёт продукт в Stripe для курса"""
        try:
            product = stripe.Product.create(
                name=course.name,
                description=course.description or "",
                metadata={"course_id": course.id},
            )
            return {"success": True, "product": product}
        except stripe.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_price(product_id, amount):
        """Создаёт цену в копейках/центах"""
        try:
            price = stripe.Price.create(
                product=product_id, unit_amount=int(amount * 100), currency="usd"
            )
            return {"success": True, "price": price}
        except stripe.StripeError as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def create_checkout_session(price_id, success_url, cancel_url, metadata):
        """Создаёт сессию оплаты"""
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price": price_id,
                        "quantity": 1,
                    }
                ],
                mode="payment",
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=metadata,
            )
            return {"success": True, "url": session.url, "session_id": session.id}
        except stripe.StripeError as e:
            return {"success": False, "error": str(e)}
