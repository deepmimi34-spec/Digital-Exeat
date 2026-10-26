
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from .forms import StudentLinkRequestForm, StudentAccessForm
from .models import Student, ParentStudentLink, StudentAccessRequest


def normalize_name(value):
    return " ".join(value.casefold().split())


@login_required
@require_http_methods(["GET", "POST"])
def link_child(request):
    if request.method == "POST":
        form = StudentLinkRequestForm(request.POST)

        if form.is_valid():
            admission_number = (
                form.cleaned_data["admission_number"].strip()
            )
            submitted_name = normalize_name(
                form.cleaned_data["full_name"]
            )

            student = None

            # Only students belonging to approved schools are eligible.
            for candidate in Student.objects.filter(
                admission_number__iexact=admission_number,
                school__status="APPROVED",
            ).select_related("school"):
                if normalize_name(candidate.full_name) == submitted_name:
                    student = candidate
                    break

            if student is not None:
                try:
                    with transaction.atomic():
                        link, created = ParentStudentLink.objects.get_or_create(
                            parent=request.user,
                            student=student,
                        )

                        if not created and link.status == (
                            ParentStudentLink.Status.REJECTED
                        ):
                            link.status = ParentStudentLink.Status.PENDING
                            link.reviewed_at = None
                            link.reviewed_by = None
                            link.requested_at = timezone.now()
                            link.save(
                                update_fields=[
                                    "status",
                                    "reviewed_at",
                                    "reviewed_by",
                                    "requested_at",
                                ]
                            )

                except IntegrityError:
                    # A concurrent request may already have created it.
                    pass

            messages.success(
                request,
                "Your request has been received if the details match "
                "a student record. The school must verify your "
                "relationship before access is granted.",
            )

            return redirect("link_child")

    else:
        form = StudentLinkRequestForm()

    return render(
        request,
        "students/link_child.html",
        {"form": form},
    )



def normalize_student_name(value):
    return " ".join(value.casefold().split())

@login_required
@require_http_methods(["GET", "POST"])
def student_access(request):
    if request.method == "POST":
        form = StudentAccessForm(request.POST)

        if form.is_valid():
            admission_number = (
                form.cleaned_data["admission_number"].strip()
            )
            submitted_name = normalize_student_name(
                form.cleaned_data["full_name"]
            )

            student = None

            candidates = Student.objects.filter(
                admission_number__iexact=admission_number,
                school__status="APPROVED",
            ).select_related("school")

            for candidate in candidates:
                if (
                    normalize_student_name(candidate.full_name)
                    == submitted_name
                ):
                    student = candidate
                    break

            if student is not None:
                access_request, created = (
                    StudentAccessRequest.objects.get_or_create(
                        user=request.user,
                        student=student,
                    )
                )

                if (
                    not created
                    and access_request.status
                    == StudentAccessRequest.Status.REJECTED
                ):
                    access_request.status = (
                        StudentAccessRequest.Status.PENDING
                    )
                    access_request.reviewed_at = None
                    access_request.reviewed_by = None
                    access_request.requested_at = timezone.now()

                    access_request.save(update_fields=[
                        "status",
                        "reviewed_at",
                        "reviewed_by",
                        "requested_at",
                    ])

            # Keep the response generic so the page does not reveal
            # whether a particular student record exists.
            messages.success(
                request,
                "Your request has been submitted if your details match "
                "a student record. Please wait for the school to verify "
                "your identity before access is granted.",
            )

            return redirect("students:student_access")

    else:
        form = StudentAccessForm()

    requests = StudentAccessRequest.objects.filter(
        user=request.user
    ).select_related("student", "student__school")

    return render(
        request,
        "students/student_access.html",
        {
            "form": form,
            "access_requests": requests,
        },
    )