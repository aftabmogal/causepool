from rest_framework import serializers
from .models import Score


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ["id", "value", "date", "created_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        qs = Score.objects.filter(user=user, date=attrs["date"])
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError(
                "A score already exists for this date. Edit or delete it instead of creating a duplicate."
            )
        return attrs
