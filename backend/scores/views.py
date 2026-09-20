from rest_framework import viewsets, permissions
from .models import Score
from .serializers import ScoreSerializer

MAX_SCORES = 5


class ScoreViewSet(viewsets.ModelViewSet):
    serializer_class = ScoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Score.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        score = serializer.save(user=self.request.user)
        # Rolling-5 logic: keep only the 5 most recent scores per user.
        qs = Score.objects.filter(user=self.request.user).order_by("-date")
        if qs.count() > MAX_SCORES:
            stale_ids = list(qs.values_list("id", flat=True)[MAX_SCORES:])
            Score.objects.filter(id__in=stale_ids).delete()
