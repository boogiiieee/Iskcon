# -*- coding: utf-8 -*-

import os
from django.conf import settings

config = {
	'autostart': False, #True or False
	'image': False, #url or False
	'start': 0, #Number
	'title': 'Title', #Text
	'description': 'description', #Text
	'controlbar': True, #True or False
	'duration': 57, #Number
	'volume': 80, #Number
	'width': 400, #Number
	'height': 400, #Number
	'events': {
		'onReady': None, #Text
		'onVolume': None, #Text
		'onError': None, #Text
		'onPlay': None, #Text
		'onPause': None, #Text
		'onSeek': None, #Text
		'onComplete': None, #Text
		'onTime': None, #Text
	}
}

DEFAULT_CONFIG = getattr(settings, 'VIDEOPLAYER_DEFAULT_CONFIG', config)