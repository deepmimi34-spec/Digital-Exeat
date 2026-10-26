
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .models import School

User = get_user_model()


class SchoolRegistrationForm(forms.Form):
    school_name = forms.CharField(max_length=200, label="School name")
    school_type = forms.ChoiceField(
        choices=School.SchoolType.choices,
        label="Type of schools",
    )
    region = forms.CharField(max_length=100)
    district = forms.CharField(max_length=100)
    address = forms.CharField(max_length=255, required=False)
    official_email = forms.EmailField()
    phone = forms.CharField(max_length=30)

    administrator_name = forms.CharField(max_length=150)
    administrator_username = forms.CharField(max_length=150)
    administrator_email = forms.EmailField()
    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
        label="Create password",
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Confirm password",
    )

    def clean_administrator_username(self):
        username = self.cleaned_data["administrator_username"].strip()

        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already in use.")

        return username

    def clean_administrator_email(self):
        email = self.cleaned_data["administrator_email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                "An account with this email already exists."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        if (
            cleaned_data.get("password")
            and cleaned_data.get("confirm_password")
            and cleaned_data["password"] != cleaned_data["confirm_password"]
        ):
            self.add_error("confirm_password", "The passwords do not match.")

        return cleaned_data


from django import forms


class SchoolLoginForm(forms.Form):
    school_name = forms.CharField(
        max_length=200,
        label="School name",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your registered school name",
            "autocomplete": "organization",
        }),
    )

    administrator_username = forms.CharField(
        max_length=150,
        label="Administrator username",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter your username",
            "autocomplete": "username",
        }),
    )

    administrator_email = forms.EmailField(
        label="Administrator email",
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter your registered email",
            "autocomplete": "email",
        }),
    )

    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "autocomplete": "current-password",
        }),
    )
