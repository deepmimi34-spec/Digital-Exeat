from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.http import require_http_methods

from .forms import SchoolRegistrationForm, SchoolLoginForm
from .models import School

User = get_user_model()


def school_signup(request):
    # Registration is public, but the administrator account is created
    # only when the submitted registration form is valid.
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
                "Your school registration has been submitted. "
                "You can access the school portal after approval.",
            )

            return redirect("schools:school_registration_pending")

    else:
        form = SchoolRegistrationForm()

    return render(
        request,
        "schools/register.html",
        {"form": form},
    )


@require_http_methods(["GET", "POST"])
def school_login(request):
    # If already signed in, route to the correct destination.
    if request.user.is_authenticated:
        return redirect("schools:dashboard")

    if request.method == "POST":
        form = SchoolLoginForm(request.POST)

        if form.is_valid():
            school_name = form.cleaned_data["school_name"].strip()
            username = form.cleaned_data["administrator_username"].strip()
            email = form.cleaned_data["administrator_email"].strip()
            password = form.cleaned_data["password"]

            # Verify the username and password.
            user = authenticate(
                request,
                username=username,
                password=password,
            )

            if (
                user is not None
                and user.email
                and user.email.casefold() == email.casefold()
            ):
                school = School.objects.filter(
                    administrator=user,
                    name__iexact=school_name,
                ).first()

                if school is not None:
                    login(request, user)

                    # The dashboard decides what this account can access.
                    return redirect("schools:dashboard")

            messages.error(
                request,
                "We could not verify your details. Please check your "
                "school name, username, email and password.",
            )
    else:
        form = SchoolLoginForm()

    return render(
        request,
        "schools/school_login.html",
        {"form": form},
    )

@staff_member_required
@require_POST
def review_school(request, school_id):
    """Allow platform staff to approve or reject school registrations."""

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

        messages.success(
            request,
            f"{school.name} has been approved.",
        )

    elif action == "reject":
        reason = request.POST.get("reason", "").strip()

        if not reason:
            messages.error(
                request,
                "Provide a reason before rejecting this school.",
            )
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

        messages.success(
            request,
            f"{school.name} has been rejected.",
        )

    else:
        messages.error(request, "Invalid review action.")

    return redirect("admin:schools_school_changelist")


def home(request):
    """Public landing page."""
    return render(request, "schools/home.html")


@login_required
def dashboard(request):
    """Direct authenticated users to the appropriate destination."""

    if request.user.is_superuser:
        return redirect("/admin/")

    school = School.objects.filter(
        administrator=request.user
    ).first()

    if school is None:
        # Users without a school account can choose another service.
        return redirect("service_selection")

    if school.status == School.ApprovalStatus.PENDING:
        return redirect("schools:dashboard_pending")

    if school.status == School.ApprovalStatus.REJECTED:
        return redirect("schools:dashboard_rejected")

    if school.status == School.ApprovalStatus.APPROVED:
        return redirect("schools:school_dashboard")

    return redirect("service_selection")


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
    """Allow approved school administrators into their school portal."""

    if request.user.is_superuser:
        return redirect("/admin/")

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


def school_registration_pending(request):
    return render(
        request,
        "schools/registration_pending.html",
    )

@login_required
def no_school_access(request):
    return render(
        request,
        "schools/no_school_access.html",
        status=403,
    )
