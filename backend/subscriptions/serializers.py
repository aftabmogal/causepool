from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    charity_name = serializers.CharField(source="charity.name", read_only=True)

    class Meta:
        model = Subscription
        fields = ["id", "plan", "status", "charity", "charity_name",
                  "charity_percentage", "renewal_date", "created_at"]
        read_only_fields = ["status", "renewal_date"]


class CheckoutSerializer(serializers.Serializer):
    plan = serializers.ChoiceField(choices=["monthly", "yearly"])
    charity_id = serializers.IntegerField()
    charity_percentage = serializers.DecimalField(max_digits=5, decimal_places=2, min_value=10, max_value=100)
