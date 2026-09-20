from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="scores", on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(45)])
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        unique_together = ("user", "date")  # one entry per date

    def __str__(self):
        return f"{self.user.username}: {self.value} on {self.date}"
