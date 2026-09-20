from rest_framework import serializers
from .models import DrawResult, Winner


class WinnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Winner
        fields = ["id", "draw", "username", "match_type", "prize_amount",
                  "proof_image", "verified", "payment_status", "created_at"]
        read_only_fields = ["prize_amount", "match_type", "draw", "verified", "payment_status"]


class DrawResultSerializer(serializers.ModelSerializer):
    winners = WinnerSerializer(many=True, read_only=True)

    class Meta:
        model = DrawResult
        fields = ["id", "month", "winning_numbers", "method", "published",
                  "prize_pool_total", "jackpot_rollover_amount", "winners"]
