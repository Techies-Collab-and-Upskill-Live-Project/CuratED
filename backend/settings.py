from pathlib import Path
from decouple import config
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Core Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = [
    "https://devcurated.vercel.app",
    "http://localhost:3000",
    "devcurated.vercel.app",
    "localhost:3000",
    'slimy-libby-htcode-d75a500b.koyeb.app',
]
CORS_ALLOWED_ORIGINS = [
    "https://devcurated.vercel.app",
    "http://localhost:3000",
    "devcurated.vercel.app",
    "localhost:3000",
]
YOUTUBE_API_KEY = config('YOUTUBE_API_KEY')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'api',
    'accounts',
    'playlists', 
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'accounts.middleware.TokenHandlerMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Specifies the custom user model for authentication.
AUTH_USER_MODEL = 'accounts.CustomUser'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_APP_PASSWORD')
DEFAULT_FROM_EMAIL = config('EMAIL_HOST_USER')


EMAIL_TEMPLATES = {
    'auth': {
        'verify_email': 'email/auth/verify_email.html',
        'password_reset': 'email/auth/password_reset.html',
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'login': '5/minute',  # Limit login attempts
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),  # Short-lived access tokens.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),     # Longer refresh tokens for user convenience.
    'ROTATE_REFRESH_TOKENS': True,                   # Generate a new refresh token upon refreshing.
    'BLACKLIST_AFTER_ROTATION': True,                # Blacklist old refresh tokens after rotation.
    'AUTH_HEADER_TYPES': ('Bearer',),
} 

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': "Enter token as: **Bearer &lt;your-token&gt;**"
        }
    },
    'USE_SESSION_AUTH': False,  # Disables Django's session authentication in Swagger UI if token authentication is preferred.
}


# Database configuration.
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': config('SUPABASE_DB_USER'),
        'PASSWORD': config('SUPABASE_DB_PASSWORD'),
        'HOST': config('SUPABASE_DB_HOST'),
        'PORT': config('SUPABASE_DB_PORT'),
        'NAME': config('SUPABASE_DB_NAME'),
    }
}


# For development, use the simpler cache backend
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Comment out Redis configuration (keep it for reference)
"""
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_PASSWORD = config('REDIS_PASSWORD')
REDIS_DB_NUMBER = config('REDIS_DB_NUMBER')

if not all([REDIS_HOST, REDIS_PORT]):
    raise ValueError("Redis host and port must be set")

# Build the location string safely
REDIS_LOCATION = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}"

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
"""

# Cache timeout settings
CACHE_TIMEOUT = 3600  # 1 hour for search results
VIDEO_DETAILS_CACHE_TIMEOUT = 86400  # 24 hours for video details

# Password validation settings.
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'accounts.validators.PasswordComplexityValidator',  # Custom validator
    }
]


# Internationalization settings.
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images) configuration.
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files configuration
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type configuration.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ensure logs directory exists
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': str(LOGS_DIR / 'debug.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# Frontend URL for password reset links
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')
