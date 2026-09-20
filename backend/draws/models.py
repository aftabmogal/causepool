from django.conf import settings
from django.db import models


class DrawResult(models.Model):
    METHOD_CHOICES = [("random", "Random"), ("weighted", "Weighted by score frequency")]

    month = models.DateField(unique=True, help_text="First day of the draw month")
    winning_numbers = models.JSONField(help_text="List of 5 unique numbers, 1-45")
    method = models.CharField(max_length=10, choices=METHOD_CHOICES, default="random")
    published = models.BooleanField(default=False)
    prize_pool_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    jackpot_rollover_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        status = "Published" if self.published else "Simulated"
        return f"Draw {self.month} ({status})"


class Winner(models.Model):
    MATCH_CHOICES = [("5", "5-Number match"), ("4", "4-Number match"), ("3", "3-Number match")]
    PAYMENT_CHOICES = [("pending", "Pending"), ("paid", "Paid")]

    draw = models.ForeignKey(DrawResult, related_name="winners", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="wins", on_delete=models.CASCADE)
    match_type = models.CharField(max_length=1, choices=MATCH_CHOICES)
    prize_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    proof_image = models.ImageField(upload_to="winner_proofs/", null=True, blank=True)
    verified = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.match_type}-match ({self.draw.month})"
