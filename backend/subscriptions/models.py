from django.conf import settings
from django.db import models


class Subscription(models.Model):
    PLAN_CHOICES = [("monthly", "Monthly"), ("yearly", "Yearly")]
    STATUS_CHOICES = [
        ("inactive", "Inactive"),
        ("active", "Active"),
        ("cancelled", "Cancelled"),
        ("lapsed", "Lapsed"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="subscription", on_delete=models.CASCADE)
    plan = models.CharField(max_length=10, choices=PLAN_CHOICES, default="monthly")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="inactive")
    stripe_customer_id = models.CharField(max_length=120, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=120, blank=True, null=True)
    charity = models.ForeignKey("charities.Charity", null=True, blank=True, on_delete=models.SET_NULL)
    charity_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=10)
    renewal_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        return self.status == "active"

    def __str__(self):
        return f"{self.user.username} - {self.plan} ({self.status})"
