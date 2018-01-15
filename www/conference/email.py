# -*- coding: utf-8 -*-

from django.db import connections

from conference.conf import *

def delete_email(email):
	u'''Функция удаления e-mail из базы данных. НЕ проверяет права пользователя.'''
	if email:
		cursor = connections[DB_MAIL_NAME].cursor()
		try:
			cursor.execute("DELETE FROM `mailbox` WHERE `username`=%s;", [ email ])
			cursor.execute("DELETE FROM `alias` WHERE `address`=%s;", [ email ])
			cursor.connection.commit()
		except: pass
		else:
			return True
	return False