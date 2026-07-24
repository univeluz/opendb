"""
OpenDB (opendb.uz) -- O'zbekiston uchun ochiq ma'lumotlar API loyihasi.
Sozlamalar python-decouple orqali .env faylidan o'qiladi (.env.example'ga qarang).
"""
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="localhost,127.0.0.1", cast=Csv())

INSTALLED_APPS = [
    # jazzmin django.contrib.admin'dan OLDIN turishi SHART
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # uchinchi tomon
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "import_export",
    # loyiha ilovalari
    "geo",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # nginx'siz statik fayllar uchun
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Ma'lumotlar bazasi ---
# docker-compose'da: POSTGRES, .env'da DB_HOST=db
# Docker'siz lokal ishga tushirishda: DB_HOST bo'sh qoldirilsa SQLite ishlatiladi.
if config("DB_HOST", default=""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME", default="opendb"),
            "USER": config("DB_USER", default="opendb"),
            "PASSWORD": config("DB_PASSWORD", default=""),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT", default="5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Django REST Framework ---
REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 50,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.AnonRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "anon": config("ANON_THROTTLE_RATE", default="1000/day"),
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "OpenDB API",
    "DESCRIPTION": "O'zbekiston uchun ochiq ma'lumotlar API -- viloyat, tuman, "
                    "bank, OTM, valyuta, bayram, telefon kodlari va boshqalar.",
    "VERSION": "1.0.0",
}

# --- django-jazzmin (admin ko'rinishi) ---
JAZZMIN_SETTINGS = {
    "site_title": "OpenDB Admin",
    "site_header": "OpenDB.uz",
    "site_brand": "OpenDB",
    "welcome_sign": "OpenDB boshqaruv paneliga xush kelibsiz",
    "copyright": "Univel",
    "search_model": ["geo.Viloyat", "geo.Tuman", "geo.Bank", "geo.OTM"],
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "geo.Viloyat": "fas fa-map-marker-alt",
        "geo.Tuman": "fas fa-map-pin",
        "geo.AholiPunkti": "fas fa-home",
        "geo.Bank": "fas fa-university",
        "geo.OTM": "fas fa-graduation-cap",
        "geo.Valyuta": "fas fa-coins",
        "geo.ValyutaKursi": "fas fa-chart-line",
        "geo.Bayram": "fas fa-calendar-star",
        "geo.BayramSanasi": "fas fa-calendar-check",
        "geo.TelefonKodi": "fas fa-phone",
    },
    "order_with_respect_to": [
        "geo.Viloyat", "geo.Tuman", "geo.AholiPunkti", "geo.Bank", "geo.OTM",
        "geo.Valyuta", "geo.ValyutaKursi", "geo.Bayram", "geo.BayramSanasi", "geo.TelefonKodi",
    ],
}
JAZZMIN_UI_TWEAKS = {"theme": "darkly"}
