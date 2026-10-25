
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .forms import SchoolRegistrationForm
from .models import School

User = get_user_model()


def school_signup(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            with transaction.atomic():
                administrator = User.objects.create_user(
                    username=data["administrator_username"],
                    email=data["administrator_email"],
                    password=data["password"],
                    first_name=data["administrator_name"],
                )

                School.objects.create(
                    name=data["school_name"],
                    school_type=data["school_type"],
                    region=data["region"],
                    district=data["district"],
                    address=data["address"],
                    official_email=data["official_email"],
                    phone=data["phone"],
                    administrator=administrator,
                    status=School.ApprovalStatus.PENDING,
                )

            messages.success(
                request,
                "Your registration has been submitted. "
                "You can sign in after your schools is approved.",
            )
            return redirect("schools:school_registration_pending")
    else:
        form = SchoolRegistrationForm()

    return render(
        request,
        "schools/register.html",
        {"form": form},
    )


def school_registration_pending(request):
    return render(
        request,
        "schools/registration_pending.html",
    )


@staff_member_required
@require_POST
def review_school(request, school_id):
    # Only platform staff can approve or reject schools registrations.
    from django.shortcuts import get_object_or_404

    school = get_object_or_404(School, pk=school_id)
    action = request.POST.get("action")

    if action == "approve":
        school.status = School.ApprovalStatus.APPROVED
        school.rejection_reason = ""
        school.reviewed_at = timezone.now()
        school.save(
            update_fields=[
                "status",
                "rejection_reason",
                "reviewed_at",
            ]
        )
        messages.success(request, f"{school.name} has been approved.")

    elif action == "reject":
        reason = request.POST.get("reason", "").strip()

        if not reason:
            messages.error(request, "Provide a reason before rejecting.")
            return redirect("admin:schools_school_changelist")

        school.status = School.ApprovalStatus.REJECTED
        school.rejection_reason = reason
        school.reviewed_at = timezone.now()
        school.save(
            update_fields=[
                "status",
                "rejection_reason",
                "reviewed_at",
            ]
        )
        messages.success(request, f"{school.name} has been rejected.")

    else:
        messages.error(request, "Invalid review action.")

    return redirect("admin:schools_school_changelist")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import School


@login_required
def school_dashboard(request):
    school = School.objects.filter(
        administrator=request.user
    ).first()

    if school is None:
        return render(
            request,
            "schools/no_school_access.html",
            status=403,
        )

    if school.status != School.ApprovalStatus.APPROVED:
        return render(
            request,
            "schools/registration_pending.html",
            status=403,
        )

    return render(
        request,
        "schools/dashboard.html",
        {"schools": school},

    )


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import School


def home(request):
    """Public landing page."""
    if request.user.is_authenticated:
        return redirect("schools:dashboard")

    return render(request, "schools/home.html")


@login_required
def dashboard(request):
    """Send each authenticated user to the appropriate destination."""

    # Platform administrator
    if request.user.is_superuser:
        return redirect("/admin/")

    # School administrator
    school = School.objects.filter(
        administrator=request.user
    ).first()

    if school:
        if school.status == School.ApprovalStatus.PENDING:
            return redirect("schools:dashboard_pending")

        if school.status == School.ApprovalStatus.REJECTED:
            return redirect("schools:dashboard_rejected")

        if school.status == School.ApprovalStatus.APPROVED:
            return redirect("schools:school_dashboard")

    # Other account types will be routed here when their roles are built.
    return render(
        request,
        "schools/no_school_access.html",
        status=403,
    )


@login_required
def dashboard_pending(request):
    school = School.objects.filter(
        administrator=request.user
    ).first()

    if school is None:
        return redirect("schools:dashboard")

    if school.status == School.ApprovalStatus.APPROVED:
        return redirect("schools:school_dashboard")

    if school.status == School.ApprovalStatus.REJECTED:
        return redirect("schools:dashboard_rejected")

    return render(
        request,
        "schools/dashboard_pending.html",
        {"school": school},
    )


@login_required
def dashboard_rejected(request):
    school = School.objects.filter(
        administrator=request.user
    ).first()

    if school is None:
        return redirect("schools:dashboard")

    if school.status == School.ApprovalStatus.APPROVED:
        return redirect("schools:school_dashboard")

    if school.status == School.ApprovalStatus.PENDING:
        return redirect("schools:dashboard_pending")

    return render(
        request,
        "schools/dashboard_rejected.html",
        {"school": school},
    )


@login_required
def school_dashboard(request):
    school = School.objects.filter(
        administrator=request.user,
        status=School.ApprovalStatus.APPROVED,
    ).first()

    if school is None:
        return redirect("schools:dashboard")

    return render(
        request,
        "schools/dashboard.html",
        {"school": school},
    )


@login_required
def no_school_access(request):
    return render(
        request,
        "schools/no_school_access.html",
        status=403,
    )
