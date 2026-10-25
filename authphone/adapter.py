
import os
import re
from django.contrib.auth import get_user_model
from django.core.exceptions import ImproperlyConfigured
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import DefaultAccountAdapter
from twilio.rest import Client

from .models import UserPhone


User = get_user_model()


class DigitalExeatAccountAdapter(DefaultAccountAdapter):
    """
    Stores phone numbers for django-allauth and sends verification
    codes using Twilio. Allauth remains responsible for code
    generation, validation, expiration and login/signup flow.
    """

    def get_phone(self, user):
        record = UserPhone.objects.filter(user=user).first()
        if not record:
            return None

        return record.phone, record.verified

    def set_phone(self, user, phone, verified):
        UserPhone.objects.update_or_create(
            user=user,
            defaults={
                "phone": phone,
                "verified": verified,
            },
        )

    def set_phone_verified(self, user, phone):
        UserPhone.objects.filter(
            user=user,
            phone=phone,
        ).update(verified=True)

    def get_user_by_phone(self, phone):
        record = (
            UserPhone.objects
            .select_related("user")
            .filter(phone=phone)
            .first()
        )
        return record.user if record else None

    def _send_sms(self, phone, message):
        account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        from_number = os.environ.get("TWILIO_FROM_NUMBER")

        if not all((account_sid, auth_token, from_number)):
            raise ImproperlyConfigured(
                "Twilio SMS settings are missing. Configure "
                "TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and "
                "TWILIO_FROM_NUMBER."
            )

        client = Client(account_sid, auth_token)
        client.messages.create(
            to=phone,
            from_=from_number,
            body=message,
        )

    def send_verification_code_sms(
        self, user, phone, code, **kwargs
    ):
        message = (
            f"Your Digital-Exeat verification code is {code}. "
            "Do not share this code. If you did not request it, "
            "you can ignore this message."
        )
        self._send_sms(phone, message)

    def send_unknown_account_sms(self, phone, **kwargs):
        # Keep this message generic to avoid revealing whether
        # a particular phone number has an account.
        self._send_sms(
            phone,
            "You requested a Digital-Exeat sign-in code. "
            "If you requested it, follow the instructions on "
            "the website. Otherwise, ignore this message.",
        )

    def clean_phone(self, phone):
        phone = super().clean_phone(phone)

        if not phone.startswith("+"):
            raise ValidationError(
                _("Enter your phone number with country code, "
                  "for example +233XXXXXXXXX.")
            )

        return phone

    def populate_username(self, request, user):
        # Allauth calls this when a required username is missing.
        if getattr(user, "username", None):
            return super().populate_username(request, user)

        phone = ""
        if request is not None:
            phone = request.POST.get("phone", "")

        digits = re.sub(r"\D", "", phone)
        base = f"parent{digits[-10:]}" if digits else "parent"

        username = base[:150]
        suffix = 1

        while User.objects.filter(username=username).exists():
            username = f"{base[:140]}{suffix}"
            suffix += 1

        user.username = username
