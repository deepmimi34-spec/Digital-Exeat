
"""
Django settings for digitalexeat.

Supports local development and Render production deployment.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured


# ==========================================================
# BASE CONFIGURATION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load local .env values without overriding variables supplied
# by the operating system or Render.
load_dotenv(BASE_DIR / ".env", override=False)


def env_bool(name, default=False):
    """Convert an environment variable into a Boolean."""
    value = os.environ.get(name)

    if value is None:
        return default

    return value.strip().lower() in {"true", "1", "yes", "on"}


RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "").strip()

IS_PRODUCTION = (
    os.environ.get("DJANGO_ENV", "").strip().lower() == "production"
    or env_bool("RENDER", False)
)

# Never allow DEBUG to be enabled in production.
DEBUG = False if IS_PRODUCTION else env_bool("DEBUG", True)


# ==========================================================
# SECRET KEY
# ==========================================================

SECRET_KEY = os.environ.get("SECRET_KEY", "").strip()

if not SECRET_KEY:
    if IS_PRODUCTION:
        raise ImproperlyConfigured(
            "SECRET_KEY must be configured in the production environment."
        )

    # Local development fallback only.
    SECRET_KEY = "django-insecure-local-development-only-change-me"


# ==========================================================
# ALLOWED HOSTS
# ==========================================================

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if host.strip()
]

if RENDER_HOST and RENDER_HOST not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_HOST)

if not IS_PRODUCTION:
    for host in ["localhost", "127.0.0.1", "[::1]"]:
        if host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(host)

if IS_PRODUCTION and not ALLOWED_HOSTS:
    raise ImproperlyConfigured(
        "Configure ALLOWED_HOSTS in the production environment."
    )


# ==========================================================
# CSRF TRUSTED ORIGINS
# ==========================================================

# ==========================================================
# CSRF TRUSTED ORIGINS
# ==========================================================

CSRF_TRUSTED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS", ""
    ).split(",")
    if origin.strip()
]

if RENDER_HOST:
    render_origin = f"https://{RENDER_HOST}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)



# ==========================================================
# APPLICATIONS
# ==========================================================

INSTALLED_APPS = [
    "unfold",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",

    # Add your own project apps here, for example:
    "schools",
    "authphone",
    "students",
    # "external_exeat",
    # "internal_exeat",
    # "announcements",
]

SITE_ID = 1


# ==========================================================
# MIDDLEWARE
# ==========================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

    "allauth.account.middleware.AccountMiddleware",
]


# ==========================================================
# URLS AND WSGI
# ==========================================================

ROOT_URLCONF = "digitalexeat.urls"
WSGI_APPLICATION = "digitalexeat.wsgi.application"


# ==========================================================
# TEMPLATES
# ==========================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==========================================================
# AUTHENTICATION
# ==========================================================

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/services/"
ACCOUNT_LOGIN_REDIRECT_URL = "/schools/dashboard/"
LOGOUT_REDIRECT_URL = "/"

ACCOUNT_LOGIN_METHODS = {"username", "email"}

ACCOUNT_SIGNUP_FIELDS = [
    "username*",
    "email*",
    "password1*",
    "password2*",
]

ACCOUNT_SESSION_REMEMBER = True

ACCOUNT_ADAPTER = "authphone.adapter.DigitalExeatAccountAdapter"



# Require phone verification.
ACCOUNT_PHONE_VERIFICATION_ENABLED = True
ACCOUNT_PHONE_VERIFICATION_MAX_ATTEMPTS = 3
ACCOUNT_PHONE_VERIFICATION_TIMEOUT = 900
ACCOUNT_PHONE_VERIFICATION_SUPPORTS_RESEND = True

# Enable this only if your registration process requires it:
# ACCOUNT_EMAIL_VERIFICATION = "mandatory"


# ==========================================================
# GOOGLE OAUTH
# ==========================================================

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "OAUTH_PKCE_ENABLED": True,
    }
}

# Social login must be initiated using POST.
SOCIALACCOUNT_LOGIN_ON_GET = False

# Configure the Google SocialApp in Django admin or through
# the allauth APPS setting. Do not configure both for the same app.


# ==========================================================
# PRODUCTION SECURITY
# ==========================================================

SECURE_SSL_REDIRECT = IS_PRODUCTION

SESSION_COOKIE_SECURE = IS_PRODUCTION
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"

CSRF_COOKIE_SECURE = IS_PRODUCTION
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"

if IS_PRODUCTION:
    # Render terminates HTTPS at its proxy.
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Start with one hour of HSTS while verifying the deployment.
SECURE_HSTS_SECONDS = 3600 if IS_PRODUCTION else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"



# ==========================================================
# DATABASE
# ==========================================================

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()

if IS_PRODUCTION and not DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL must point to your production database."
    )

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ==========================================================
# PASSWORD VALIDATION
# ==========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
        "OPTIONS": {"min_length": 12},
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ==========================================================
# EMAIL
# ==========================================================

if IS_PRODUCTION:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

    EMAIL_HOST = os.environ.get("EMAIL_HOST", "").strip()
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "").strip()
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
    EMAIL_USE_SSL = env_bool("EMAIL_USE_SSL", False)
    EMAIL_TIMEOUT = 30

    DEFAULT_FROM_EMAIL = os.environ.get(
        "DEFAULT_FROM_EMAIL", ""
    ).strip()

    if EMAIL_USE_TLS and EMAIL_USE_SSL:
        raise ImproperlyConfigured(
            "EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be enabled."
        )

    if not all([
        EMAIL_HOST,
        EMAIL_HOST_USER,
        EMAIL_HOST_PASSWORD,
        DEFAULT_FROM_EMAIL,
    ]):
        raise ImproperlyConfigured(
            "Configure EMAIL_HOST, EMAIL_HOST_USER, "
            "EMAIL_HOST_PASSWORD and DEFAULT_FROM_EMAIL."
        )

else:
    # Emails are printed in the terminal during development.
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    DEFAULT_FROM_EMAIL = "deepmimi34@gmail.com"


# ==========================================================
# INTERNATIONALIZATION
# ==========================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Accra"

USE_I18N = True
USE_TZ = True


# ==========================================================
# STATIC FILES
# ==========================================================


STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}


# ==========================================================
# DJANGO UNFOLD ADMIN
# ==========================================================

UNFOLD = {
    "SITE_TITLE": "Digital Exeat Management System",
    "SITE_DESCRIPTION": "Digital Exeat Management System",
    "SITE_HEADER": "Digital Exeat Management System",
    "SITE_SUBHEADER": "Exeat Administration",
    "SITE_URL": "/help",
    "SITE_SYMBOL": "monitor",
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
}


# ==========================================================
# DEFAULT PRIMARY KEY
# ==========================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
