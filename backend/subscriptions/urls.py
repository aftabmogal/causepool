from django.urls import path
from .views import MySubscriptionView, CreateCheckoutSessionView, CancelSubscriptionView, stripe_webhook

urlpatterns = [
    path("me/", MySubscriptionView.as_view(), name="my-subscription"),
    path("checkout/", CreateCheckoutSessionView.as_view(), name="checkout"),
    path("cancel/", CancelSubscriptionView.as_view(), name="cancel-subscription"),
    path("webhook/", stripe_webhook, name="stripe-webhook"),
]
