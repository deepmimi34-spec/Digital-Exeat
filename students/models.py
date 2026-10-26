
from django.conf import settings
from django.db import models


class Student(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.PROTECT,
        related_name="students",
    )
    admission_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    other_names = models.CharField(max_length=150, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["school", "admission_number"],
                name="unique_student_admission_per_school",
            ),
        ]

    @property
    def full_name(self):
        return " ".join(
            part for part in [
                self.first_name,
                self.other_names,
                self.last_name,
            ] if part
        )

    def __str__(self):
        return f"{self.admission_number} - {self.full_name}"


class ParentStudentLink(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Verification"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_link_requests",
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.PROTECT,
        related_name="parent_link_requests",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_student_links",
    )

    class Meta:
        ordering = ["-requested_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "student"],
                name="unique_parent_student_link_request",
            ),
        ]

    def __str__(self):
        return f"{self.parent} - {self.student} ({self.status})"



class StudentAccessRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending Verification"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_access_requests",
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="access_requests",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_student_access_requests",
    )

    class Meta:
        ordering = ["-requested_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "student"],
                name="unique_student_access_request",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.student} ({self.status})"