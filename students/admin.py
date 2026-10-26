
from django.contrib import admin

from .models import Student, ParentStudentLink, StudentAccessRequest


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "admission_number",
        "first_name",
        "last_name",
        "school",
    )
    search_fields = (
        "admission_number",
        "first_name",
        "last_name",
        "school__name",
    )
    list_filter = ("school",)


@admin.register(ParentStudentLink)
class ParentStudentLinkAdmin(admin.ModelAdmin):
    list_display = (
        "parent",
        "student",
        "status",
        "requested_at",
    )
    list_filter = ("status", "student__school")
    search_fields = (
        "parent__username",
        "parent__email",
        "student__admission_number",
        "student__first_name",
        "student__last_name",
    )
    readonly_fields = (
        "parent",
        "student",
        "requested_at",
    )

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(StudentAccessRequest)
class StudentAccessRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "student",
        "status",
        "requested_at",
        "reviewed_at",
    )

    list_filter = (
        "status",
        "student__school",
    )

    search_fields = (
        "user__username",
        "user__email",
        "student__admission_number",
        "student__first_name",
        "student__last_name",
        "student__school__name",
    )

    readonly_fields = (
        "user",
        "student",
        "requested_at",
    )