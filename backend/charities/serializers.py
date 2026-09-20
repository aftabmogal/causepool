from rest_framework import serializers
from .models import Charity, CharityEvent


class CharityEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharityEvent
        fields = ["id", "title", "date", "location", "description"]


class CharitySerializer(serializers.ModelSerializer):
    events = CharityEventSerializer(many=True, read_only=True)

    class Meta:
        model = Charity
        fields = ["id", "name", "slug", "tagline", "description", "image_url",
                  "is_featured", "is_active", "events"]
