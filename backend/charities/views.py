from rest_framework import viewsets, permissions, filters
from .models import Charity
from .serializers import CharitySerializer


class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.filter(is_active=True)
    serializer_class = CharitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "description", "tagline"]
    lookup_field = "slug"
