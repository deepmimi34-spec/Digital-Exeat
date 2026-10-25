from django.contrib import admin

from .models import UserPhone


@admin.register(UserPhone)
class UserPhoneAdmin(admin.ModelAdmin):
    list_display = ("user", "masked_phone", "verified", "updated_at")
    list_filter = ("verified",)
    search_fields = ("user__username",)
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Phone")
    def masked_phone(self, obj):
        return f"••••{obj.phone[-4:]}"