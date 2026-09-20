import json
import stripe
from datetime import timedelta
from django.conf import settings
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from charities.models import Charity
from .models import Subscription
from .serializers import SubscriptionSerializer, CheckoutSerializer
from .stripe_utils import create_checkout_session

stripe.api_key = settings.STRIPE_SECRET_KEY


class MySubscriptionView(generics.RetrieveAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        sub, _ = Subscription.objects.get_or_create(user=self.request.user)
        return sub


class CreateCheckoutSessionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        charity = Charity.objects.filter(id=data["charity_id"]).first()
        if not charity:
            return Response({"detail": "Charity not found"}, status=404)

        # NOTE: requires real Stripe test-mode price IDs configured in env.
        # If not configured yet, we still update local state so the rest
        # of the app (scores/dashboard/draws) is fully testable end to end.
        sub, _ = Subscription.objects.get_or_create(user=request.user)
        sub.plan = data["plan"]
        sub.charity = charity
        sub.charity_percentage = data["charity_percentage"]

        if settings.STRIPE_SECRET_KEY and settings.STRIPE_PRICE_MONTHLY:
            session = create_checkout_session(
                request.user, data["plan"], charity.id, data["charity_percentage"]
            )
            sub.save()
            return Response({"checkout_url": session.url})
        else:
            # Dev fallback: mark active immediately so the flow is testable
            # without live Stripe keys during development.
            sub.status = "active"
            sub.renewal_date = timezone.now().date() + (
                timedelta(days=365) if data["plan"] == "yearly" else timedelta(days=30)
            )
            sub.save()
            return Response({"checkout_url": None, "detail": "Activated in dev mode (no Stripe keys set)."})


class CancelSubscriptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        sub = Subscription.objects.filter(user=request.user).first()
        if not sub:
            return Response({"detail": "No subscription"}, status=404)
        sub.status = "cancelled"
        if sub.stripe_subscription_id and settings.STRIPE_SECRET_KEY:
            try:
                stripe.Subscription.delete(sub.stripe_subscription_id)
            except Exception:
                pass
        sub.save()
        return Response(SubscriptionSerializer(sub).data)


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE", "")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    etype = event["type"]
    obj = event["data"]["object"]

    if etype == "checkout.session.completed":
        meta = obj.get("metadata", {})
        user_id = meta.get("user_id")
        if user_id:
            sub = Subscription.objects.filter(user_id=user_id).first()
            if sub:
                sub.status = "active"
                sub.stripe_subscription_id = obj.get("subscription")
                sub.charity_id = meta.get("charity_id") or sub.charity_id
                sub.charity_percentage = meta.get("charity_percentage") or sub.charity_percentage
                sub.renewal_date = timezone.now().date() + (
                    timedelta(days=365) if meta.get("plan") == "yearly" else timedelta(days=30)
                )
                sub.save()

    elif etype in ("customer.subscription.deleted",):
        sub = Subscription.objects.filter(stripe_subscription_id=obj.get("id")).first()
        if sub:
            sub.status = "lapsed"
            sub.save()

    return HttpResponse(status=200)
