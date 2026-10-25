
from django.conf import settings
from django.db import models


class UserPhone(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auth_phone",
    )
    phone = models.CharField(max_length=16, unique=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Avoid displaying the complete phone number in admin lists.
        return f"Phone account for user {self.user_id}"
