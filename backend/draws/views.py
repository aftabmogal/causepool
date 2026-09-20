from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from .models import DrawResult, Winner
from .serializers import DrawResultSerializer, WinnerSerializer


class DrawResultViewSet(viewsets.ReadOnlyModelViewSet):
    """Publicly viewable published draws; admins manage draws via /admin/."""
    serializer_class = DrawResultSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = DrawResult.objects.all().order_by("-month")
        if not (self.request.user.is_authenticated and self.request.user.is_staff):
            qs = qs.filter(published=True)
        return qs


class MyWinsViewSet(viewsets.ModelViewSet):
    serializer_class = WinnerSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        return Winner.objects.filter(user=self.request.user).order_by("-created_at")

    @action(detail=True, methods=["post"])
    def upload_proof(self, request, pk=None):
        winner = self.get_object()
        file = request.FILES.get("proof_image")
        if not file:
            return Response({"detail": "proof_image file required"}, status=400)
        winner.proof_image = file
        winner.save()
        return Response(WinnerSerializer(winner).data)
