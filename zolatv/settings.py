import os
from pathlib import Path
from zolatv.config import config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config["SECRET_KEY"]

DEBUG = config["DEBUG"]

ALLOWED_HOSTS = config["ALLOWED_HOSTS"]
AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = (
    # 'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    'users.backends.PhoneOrEmailBackend',
)

INSTALLED_APPS = [
    'modeltranslation',
    'django.contrib.admin',
    'admin_reorder',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'main.apps.MainConfig',
    'analytics.apps.AnalyticsConfig',
    'social_django',
    'social.apps.django_app.default'
]
SOCIAL_AUTH_GOOGLE_OAUTH_KEY = config["SOCIAL_AUTH_GOOGLE_OAUTH_KEY"]
SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = config["SOCIAL_AUTH_GOOGLE_OAUTH_SECRET"]

SOCIAL_AUTH_FACEBOOK_KEY = config["SOCIAL_AUTH_FACEBOOK_KEY"]
SOCIAL_AUTH_FACEBOOK_SECRET = config["SOCIAL_AUTH_FACEBOOK_SECRET"]

SOCIAL_AUTH_TWITTER_KEY = config["SOCIAL_AUTH_TWITTER_KEY"]
SOCIAL_AUTH_TWITTER_SECRET = config["SOCIAL_AUTH_TWITTER_SECRET"]

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
SOCIAL_AUTH_LOGIN_URL = '/'

ADMIN_REORDER = (
    {'app': 'admin', 'label': 'Администрирование',
     'models': (
         {'model': 'admin.LogEntry', 'label': 'Админ логи'},
         {'model': 'auth.Group', 'label': 'Группы пользователей (АДМ)'},
     )
     },
    {'app': 'analytics', 'label': 'Аналитика',
     'models': (
         'analytics.BannerAnalytics',
         'analytics.EventAnalytics',
         'analytics.FirstAnalytics',
     )
     },
    {'app': 'main', 'label': 'Реклама',
     'models': (
         'main.Adbanner',
         'main.AdVideo',
         'main.AdVideoBanner',
         'main.AdVideoMidroll',
         'main.Setting',
         'main.Popup',
     )
     },
    {'app': 'main', 'label': 'Фильмы',
     'models': (
         'main.Movie',
         'main.MovieAltLang',
     )
     },
    {'app': 'main', 'label': 'Сериалы',
     'models': (
         'main.Serie',
         'main.SerieSeason',
         'main.SerieEpisode',
         'main.SerieEpAltLang',
     )
     },
    {'app': 'main', 'label': 'Тв-Шоу',
     'models': (
         'main.Show',
         'main.ShowSeason',
         'main.ShowEpisode',
     )
     },
    {'app': 'main', 'label': 'Каналы',
     'models': (
         'main.Channel',
         'main.ChannelProvider',
     )
     },
    {'app': 'main', 'label': 'Спорт',
     'models': (
         'main.Sport',
         'main.SportKind',
     )
     },
    {'app': 'main', 'label': 'Подборки',
     'models': (
         'main.Movielist',
         'main.Serielist',
         'main.Showlist',
         'main.Channellist',
         'main.Sportlist',
     )
     },
    {'app': 'main', 'label': 'Страницы',
     'models': (
         'main.Page',
         'main.Component',
     )
     },
    {'app': 'main', 'label': 'Доп. модели',
     'models': (
         'main.Genre',
         'main.Country',
         'main.Language',
         'main.Subtitle',
     )
     },
    {'app': 'users', 'label': 'Пользователи',
     'models': (
         'users.CustomUser',
         'users.UserProfile',
         'users.CodeActivation',
         'users.UserGroup',
         'users.AppRating',
         'users.RefLink',
     )
     },
    {'app': 'users', 'label': 'Активность пользователей',
     'models': (
         'users.UserWatchHisory',
         'users.UserWatchList',
         'users.UserFeedback',
         'users.Subscription',
         'users.UserSubscription',
         'users.Comment',
         'users.CommentLike',
         'users.Rating',
     )
     },
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
    'main.middleware.timing',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middlewares.IpHandlerMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'zolatv.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'zolatv.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config["database"]["NAME"],
        'USER': config["database"]["USER"],
        'PASSWORD': config["database"]["PASSWORD"],
        'HOST': config["database"]["HOST"],
        'PORT': config["database"]["PORT"],
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
print(LOCALE_PATHS)

LANGUAGE_CODE = 'en'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('en', gettext('English')),
    ('hi', gettext('Hindi'))
)
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SOCIAL_AUTH_JSONFIELD_ENABLED = True

EMAIL_USE_TLS = True
EMAIL_HOST = config["EMAIL_HOST"]
EMAIL_HOST_USER = config["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = config["EMAIL_HOST_PASSWORD"]
EMAIL_PORT = config["EMAIL_PORT"]
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SMS_BACKEND = 'sms.backends.twilio.SmsBackend'
TWILIO_ACCOUNT_SID = config["TWILIO_ACCOUNT_SID"]
TWILIO_AUTH_TOKEN = config["TWILIO_AUTH_TOKEN"]
TWILIO_PHONE_NUMBER = config["TWILIO_PHONE_NUMBER"]

SHOW_HEADERS = True
SHOW_FOOTERS = True
ITS_APP = False
CLON_APP = False

DJANGO_ADMIN_LOGS_DELETABLE = True
DJANGO_ADMIN_LOGS_ENABLED = True

NO_REDIRECT_PATHS = [
    '/il8n/',
    '/media/',
    '/static/',
    '/admin',
    '/admin/',
    '/analytics',
    '/analytics/',
    '/analyt',
    '/analyt/',
]
