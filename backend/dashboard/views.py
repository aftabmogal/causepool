from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from subscriptions.models import Subscription
from scores.models import Score
from draws.models import DrawResult, Winner


class UserDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        sub = Subscription.objects.filter(user=user).first()
        scores = Score.objects.filter(user=user).order_by("-date")
        wins = Winner.objects.filter(user=user).order_by("-created_at")
        upcoming_draw = DrawResult.objects.filter(published=False).order_by("month").first()
        entered_draws = DrawResult.objects.filter(published=True).count() if sub and sub.is_active else 0

        return Response({
            "subscription": {
                "status": sub.status if sub else "inactive",
                "plan": sub.plan if sub else None,
                "renewal_date": sub.renewal_date if sub else None,
                "charity": sub.charity.name if sub and sub.charity else None,
                "charity_percentage": sub.charity_percentage if sub else None,
            },
            "scores": [{"value": s.value, "date": s.date} for s in scores],
            "participation": {
                "draws_entered": entered_draws,
                "next_draw_month": upcoming_draw.month if upcoming_draw else None,
            },
            "winnings": {
                "total_won": sum(w.prize_amount for w in wins),
                "pending": sum(w.prize_amount for w in wins if w.payment_status == "pending"),
                "paid": sum(w.prize_amount for w in wins if w.payment_status == "paid"),
                "records": [
                    {"draw_month": w.draw.month, "match_type": w.match_type,
                     "amount": w.prize_amount, "status": w.payment_status}
                    for w in wins
                ],
            },
        })


class AdminAnalyticsView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.contrib.auth import get_user_model
        User = get_user_model()

        return Response({
            "total_users": User.objects.count(),
            "active_subscribers": Subscription.objects.filter(status="active").count(),
            "total_prize_pool_paid": sum(
                w.prize_amount for w in Winner.objects.filter(payment_status="paid")
            ),
            "total_prize_pool_pending": sum(
                w.prize_amount for w in Winner.objects.filter(payment_status="pending")
            ),
            "draws_run": DrawResult.objects.filter(published=True).count(),
        })
