# -*- coding: utf-8 -*-

import os
def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('gva', 'gladkiyva@gmail.com'),
    ('poa', 'poa.webaspect@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'iskcon_test',
        'USER': 'postgres',                    
        'PASSWORD': '',                
        'HOST': 'localhost',                     
        'PORT': '5432',                   
    },
    # 'mail': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'vmail',
    #     'USER': 'root',
    #     'PASSWORD': 'Ghbdtn!',
    #     'HOST': '62.64.24.29',
    #     'PORT': '3306',
    # },
}

TIME_ZONE = 'Asia/Novosibirsk'
LANGUAGE_CODE = 'ru'

SITE_ID = 1

USE_I18N = True
USE_L10N = True

MEDIA_ROOT = rel('media')
STATIC_ROOT = rel('static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

# ADMIN_MEDIA_PREFIX = '/static/admin/'

STATICFILES_DIRS = ()

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

SECRET_KEY = '4ms(ow711j_(d0m&amp;g7sm4%a#h!rn@&amp;za0%9slg#38#$snt-+i0'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'my_flatpages.middleware.FlatpageFallbackMiddleware',
    # 'configuration.middleware.ConfigurationMiddleware',
)

ROOT_URLCONF = 'www.urls'

WSGI_APPLICATION = 'www.wsgi.application'

TEMPLATE_DIRS = (
    rel('..', 'admin_tools_ru', 'templates'),
    rel('templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',

    # django 1.2 only
    'django.contrib.messages.context_processors.messages',

    # required by django-admin-tools
    'django.core.context_processors.request',
    'configuration.context_processors.custom_proc',
    'iskcon.context_processors.custom_proc',
)

INSTALLED_APPS = (
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.sitemaps',
    
    'django.contrib.comments',
    
    'admin_tools_ru',
    'engine',
    'news',
    'feedback',
    'paginator',
    'registration',
    'my_flatpages',
    'configuration',
    'copyright',
    'iskcon', 
    'article',
    'media_content',
    'videoplayer',
    'forum',
    'ad_board',
    'electronic_catalog',
    #'multicasting',
    'conference',
    
    'markdown',
    'markitup',
    
    'redactor',
    'widget_tweaks',
    'pytils',
    'pymorphy',
    'annoying',
    # 'django_cleanup',
    'sorl.thumbnail',
    'debug_toolbar',
    'mptt',
    'captcha',
    'south',
    'adv_cache_tag',
    'django_mailbox',
    'djangoformsetjs',
    'permissions_widget',
    'private_media',
    'embed_video',
    
    'sslserver',
)

PERMISSIONS_WIDGET_EXCLUDE_APPS = [
    'sessions',
    
    'admin_tools',
    'theming',
    'menu',
    'dashboard',
    'south',
    'captcha',
    'django_mailbox',
]

PROTOKOL = 'https://'

REDACTOR_OPTIONS = {'lang': 'ru',}

MARKITUP_SET = 'markitup/sets/markdown'
MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})

AUTH_PROFILE_MODULE = 'iskcon.UserProfile'

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 2

CACHE_TABLE = 'cache_table'
CACHES = {
    'default': {
        # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': CACHE_TABLE,
    }
}
ADV_CACHE_VERSIONING =True
ADV_CACHE_INCLUDE_PK = True
ADV_CACHE_COMPRESS = True
ADV_CACHE_COMPRESS_SPACES = True

FORUM_BASE = '/forum'
FORUM_MAIL_PREFIX = u'[Форум]'
FORUM_PAGINATION = 20
PAGINATE_BY = 10

ADMIN_TOOLS_THEMING_CSS = 'admin_tools/css/theming_webaspect.css'
ADMIN_TOOLS_MENU = 'www.dashboard.CustomMenuDashboard'
ADMIN_TOOLS_INDEX_DASHBOARD = 'www.dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'www.dashboard.CustomAppIndexDashboard'

PYMORPHY_DICTS = {
    'ru': { 'dir': os.path.join(MEDIA_ROOT, 'morphy_ru') },
}

DEFAULT_FROM_EMAIL = 'info@iskcon.tomsk.ru'
EMAIL_HOST = '62.64.24.29'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'info@iskcon.tomsk.ru'
EMAIL_HOST_PASSWORD = 'HjsGh71Hjs'
EMAIL_USE_TLS = True

DJANGO_MAILBOX_ADMIN_ENABLED = True

PRIVATE_MEDIA_URL = '/private/'
PRIVATE_MEDIA_ROOT = rel('private')
PRIVATE_MEDIA_SERVER = 'private_media.servers.DefaultServer'
PRIVATE_MEDIA_PERMISSIONS = 'conference.permissions.MailboxPkPermissions'

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.version.VersionDebugPanel',
    'debug_toolbar.panels.timer.TimerDebugPanel',
    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
    'debug_toolbar.panels.headers.HeaderDebugPanel',
    'debug_toolbar.panels.profiling.ProfilingDebugPanel',
    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
    'debug_toolbar.panels.sql.SQLDebugPanel',
    'debug_toolbar.panels.template.TemplateDebugPanel',
    'debug_toolbar.panels.cache.CacheDebugPanel',
    'debug_toolbar.panels.signals.SignalDebugPanel',
    'debug_toolbar.panels.logger.LoggingPanel',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

MPTT_ADMIN_LEVEL_INDENT = 40

ALLOWED_TAGS = [
    'html',
    'head',
    'title',
    'meta',
    'body',
    'a',
    'abbr',
    'acronym',
    'b',
    'blockquote',
    'code',
    'em',
    'i',
    'li',
    'ol',
    'strong',
    'ul',
    'img',
    'p',
    'span',
    'div',
    'u',
    'font',
    'strike',
    'br',
    'hr',
    'pre',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'table', 'tr', 'td', 'th', 'thead', 'tbody',
    'iframe',
    'object',
    'param',
    'embed',
]

ALLOWED_ATTRIBUTES = {
    '*': ['id', 'class', 'style', 'align'],
    'a': ['href', 'title',],
    'abbr': ['title'],
    'acronym': ['title'],
    'img': ['src', 'alt', 'unselectable'],
    'table': ['width', 'height', 'border'],
    'tr': ['rowspan', 'height'],
    'td': ['colspan', 'width'],
    'th': ['colspan', 'width'],
    'font': ['color', 'face', 'size'],
    'iframe': ['width', 'height', 'src', 'frameborder', 'allowfullscreen'],
    'object': ['width', 'height'],
    'param': ['name', 'value'],
    'embed': ['src', 'type', 'width', 'height', 'allowscriptaccess', 'allowfullscreen'],
}

ALLOWED_STYLES = [
    'font-family',
    'font-size',
    'line-height',
    'height',
    'wight',
    'margin',
    'padding',
    'float',
    'border',
    'color',
    'background-color',
    'text-align',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': rel('..', 'log.txt'),
            'maxBytes': 50000,
            'backupCount': 2,
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'threadmail': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'django_mail': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}
