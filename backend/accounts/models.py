from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user so we can extend later without migration pain."""
    is_admin_role = models.BooleanField(default=False)

    def __str__(self):
        return self.username
