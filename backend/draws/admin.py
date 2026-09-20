from decimal import Decimal
from django.contrib import admin
from django.utils import timezone
from django.conf import settings
from .models import DrawResult, Winner


class WinnerInline(admin.TabularInline):
    model = Winner
    extra = 0
    readonly_fields = ["user", "match_type", "prize_amount"]


@admin.register(DrawResult)
class DrawResultAdmin(admin.ModelAdmin):
    list_display = ["month", "method", "published", "prize_pool_total", "jackpot_rollover_amount"]
    inlines = [WinnerInline]
    actions = ["publish_draw"]

    def publish_draw(self, request, queryset):
        from subscriptions.models import Subscription
        SHARES = {"5": Decimal("0.40"), "4": Decimal("0.35"), "3": Decimal("0.25")}

        for draw in queryset:
            if draw.published:
                continue
            active_subs = Subscription.objects.filter(status="active").select_related("user")
            total_pool = sum(
                Decimal(settings.SUBSCRIPTION_FEES[s.plan]) * (s.charity_percentage / Decimal(100)).__rsub__(1)
                for s in active_subs
            ) if active_subs else Decimal(0)
            # total_pool above = subscription fees minus charity cut, summed
            draw.prize_pool_total = total_pool

            winning_set = set(draw.winning_numbers)
            winners_by_tier = {"5": [], "4": [], "3": []}

            for sub in active_subs:
                user_scores = set(sub.user.scores.values_list("value", flat=True))
                if len(user_scores) < 5:
                    continue
                match_count = len(user_scores & winning_set)
                if match_count >= 3:
                    winners_by_tier[str(match_count)].append(sub.user)

            for tier, users in winners_by_tier.items():
                tier_pool = total_pool * SHARES[tier] + (draw.jackpot_rollover_amount if tier == "5" else 0)
                if tier == "5" and not users:
                    draw.jackpot_rollover_amount = tier_pool  # rolls over untouched
                    continue
                if not users:
                    continue
                split = tier_pool / len(users)
                for user in users:
                    Winner.objects.create(draw=draw, user=user, match_type=tier, prize_amount=split)
                if tier == "5":
                    draw.jackpot_rollover_amount = Decimal(0)

            draw.published = True
            draw.published_at = timezone.now()
            draw.save()

    publish_draw.short_description = "Publish selected draw(s): compute winners & prize splits"


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["user", "draw", "match_type", "prize_amount", "verified", "payment_status"]
    list_filter = ["match_type", "verified", "payment_status"]
    actions = ["mark_verified", "mark_paid"]

    def mark_verified(self, request, queryset):
        queryset.update(verified=True)
    mark_verified.short_description = "Mark selected winners as verified"

    def mark_paid(self, request, queryset):
        queryset.filter(verified=True).update(payment_status="paid")
    mark_paid.short_description = "Mark verified winners as paid"
