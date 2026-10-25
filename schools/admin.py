
from django.contrib import admin
from django.utils import timezone

from unfold.admin import ModelAdmin
from .models import School


@admin.register(School)
class SchoolAdmin(ModelAdmin):
    list_display = (
        "name",
        "school_type",
        "region",
        "official_email",
        "status",
        "created_at",
    )

    list_filter = ("status", "school_type", "region")
    search_fields = (
        "name",
        "official_email",
        "phone",
        "administrator__username",
        "administrator__email",
    )
    readonly_fields = ("created_at", "reviewed_at")
    list_per_page = 25

    actions = ["approve_selected_schools"]

    @admin.action(description="Approve selected schools registrations")
    def approve_selected_schools(self, request, queryset):
        count = queryset.exclude(
            status=School.ApprovalStatus.APPROVED
        ).update(
            status=School.ApprovalStatus.APPROVED,
            rejection_reason="",
            reviewed_at=timezone.now(),
        )
        self.message_user(request, f"{count} schools(s) approved.")
