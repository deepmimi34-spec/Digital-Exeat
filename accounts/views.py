from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def service_selection(request):
    """Show available services to authenticated users."""
    return render(
        request,
        "accounts/service_selection.html",
    )