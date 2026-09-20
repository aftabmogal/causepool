import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

PRICE_MAP = {
    "monthly": lambda: settings.STRIPE_PRICE_MONTHLY,
    "yearly": lambda: settings.STRIPE_PRICE_YEARLY,
}


def get_or_create_customer(user):
    from .models import Subscription
    sub, _ = Subscription.objects.get_or_create(user=user)
    if sub.stripe_customer_id:
        return sub.stripe_customer_id, sub
    customer = stripe.Customer.create(email=user.email or None, name=user.username)
    sub.stripe_customer_id = customer["id"]
    sub.save(update_fields=["stripe_customer_id"])
    return customer["id"], sub


def create_checkout_session(user, plan, charity, charity_percentage):
    customer_id, sub = get_or_create_customer(user)
    price_id = PRICE_MAP[plan]()
    session = stripe.checkout.Session.create(
        customer=customer_id,
        mode="subscription",
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=f"{settings.FRONTEND_URL}/dashboard?checkout=success",
        cancel_url=f"{settings.FRONTEND_URL}/subscribe?checkout=cancelled",
        metadata={"user_id": user.id, "charity_id": charity, "charity_percentage": str(charity_percentage), "plan": plan},
    )
    return session
