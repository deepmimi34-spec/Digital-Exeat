
from django.conf import settings
from django.db import models


class School(models.Model):
    class SchoolType(models.TextChoices):
        MIDDLE = "MIDDLE", "Middle School"
        SHS = "SHS", "Senior High School"
        BASIC = "BASIC", "Basic School"
        OTHER = "OTHER", "Other"

    class ApprovalStatus(models.TextChoices):
        PENDING = "PENDING", "Pending Approval"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    name = models.CharField(max_length=200)
    school_type = models.CharField(
        max_length=20,
        choices=SchoolType.choices,
    )
    region = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=255, blank=True)
    official_email = models.EmailField()
    phone = models.CharField(max_length=30)

    administrator = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="managed_school",
    )
    nickname = models.CharField(
        max_length=50,
        unique=True,
        help_text="Short name students and parents recognize, e.g. Botwe.",
    )

    logo = models.ImageField(
        upload_to="school_logos/",
        blank=True,
        null=True,
    )
    status = models.CharField(
        max_length=20,
        choices=ApprovalStatus.choices,
        default=ApprovalStatus.PENDING,
    )
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.status})"
