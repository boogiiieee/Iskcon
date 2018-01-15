# -*- coding: utf-8 -*-

from www.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'iskcon',                     
        'USER': 'pgadmin',                    
        'PASSWORD': 'asdqwe123',                
        'HOST': 'localhost',                     
        'PORT': '5432',                   
    },
	'mail': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'vmail',
		'USER': 'root',
		'PASSWORD': 'Ghbdtn!',
		'HOST': '62.64.24.29',
		'PORT': '3306',
	},
}

DEFAULT_FROM_EMAIL = 'info@iskcon.tomsk.ru'
EMAIL_HOST = '62.64.24.29'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'info@iskcon.tomsk.ru'
EMAIL_HOST_PASSWORD = 'HjsGh71Hjs'
EMAIL_USE_TLS = True

DJANGO_MAILBOX_ADMIN_ENABLED = False