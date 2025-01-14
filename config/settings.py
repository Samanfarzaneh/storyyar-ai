from pathlib import Path
from decouple import config

# تعریف BASE_DIR
BASE_DIR = Path(__file__).resolve().parent.parent

# امنیت
SECRET_KEY = config('SECRET_KEY')

# حالت دیباگ
DEBUG = config('DEBUG', default=False, cast=bool)

# هاست‌های مجاز
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# اپلیکیشن‌های نصب شده
INSTALLED_APPS = [
    'rest_framework',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'image_processor',  # نام اپلیکیشن خود را وارد کنید
]

# میان‌افزارها
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# تنظیمات URL
ROOT_URLCONF = 'config.urls'

# قالب‌ها
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI
WSGI_APPLICATION = 'config.wsgi.application'

# تنظیمات دیتابیس با mysql-connector-python
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='3306'),
        'OPTIONS': {
            'autocommit': True,
        },
    }
}

# اعتبارسنجی رمز عبور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# بین‌المللی‌سازی
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# فایل‌های استاتیک
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = BASE_DIR / 'static'

# فایل‌های مدیا
MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = BASE_DIR / 'media'

# نوع پیش‌فرض کلید اصلی
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# مسیر مدل
MODEL_PATH = config('MODEL_PATH', default=BASE_DIR / "model" / "inswapper_128.onnx")

# تنظیمات امنیتی اختیاری برای تولید
SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=False, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
X_FRAME_OPTIONS = 'DENY'
