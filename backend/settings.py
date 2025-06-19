from pathlib import Path
from decouple import config
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Core Settings
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')
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
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'accounts.middleware.TokenHandlerMiddleware',
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
EMAIL_HOST = 'smtp.resend.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = config('RESEND_SMTP_USER', default='noreply@yourdomain.com')  # Use your verified sender email
EMAIL_HOST_PASSWORD = config('RESEND_API_KEY')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = config('RESEND_SMTP_USER', default='noreply@yourdomain.com')

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
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#         'LOCATION': 'unique-snowflake',
#     }
# }

# Production Redis Configuration (using Redis Enterprise Cloud or similar)
# REDIS_HOST = config('REDIS_HOST', default='127.0.0.1')
# REDIS_PORT = config('REDIS_PORT', default='6379', cast=int)
# REDIS_PASSWORD = config('REDIS_PASSWORD', default=None)
# REDIS_DB_NUMBER = config('REDIS_DB_NUMBER', default='0', cast=int)

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': f'rediss://{":" + REDIS_PASSWORD + "@" if REDIS_PASSWORD else ""}{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}',
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'CONNECTION_POOL_KWARGS': {
#                 'ssl_cert_reqs': None,
#                 'socket_connect_timeout': 15,  # seconds, default is usually 5 or None
#                 'socket_timeout': 15,          # seconds, for read/write operations
#             }
#         }
#     }
# }

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379',  # Adjust Redis URL as needed
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

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

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type configuration.
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ensure logs directory exists
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

# Email templates directory
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']

# Frontend URL for password reset links
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

# Email templates directory
TEMPLATES[0]['DIRS'] = [BASE_DIR / 'templates']
