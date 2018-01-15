# -*- coding: utf-8 -*-

DB_MAIL_NAME = u'mail' #Название БД в settings.py

MAIL_EXLUDE_LOGIN = [
    u'root@iskcon.tomsk.ru', u'admin@iskcon.tomsk.ru',
    u'administrator@iskcon.tomsk.ru', u'test@iskcon.tomsk.ru',
    u'info@iskcon.tomsk.ru', u'help@iskcon.tomsk.ru',
    u'support@iskcon.tomsk.ru', u'helper@iskcon.tomsk.ru'
]

MAIL_SERVER_INTERFACE = 'https://mail.iskcon.tomsk.ru/mail/'
MAIL_DOMAIN = 'iskcon.tomsk.ru' # Часть домена для составления логина почтового ящика.

#Настройки подключения к почтовому серверу приложения
MAIL_SERVER = 'mail.iskcon.tomsk.ru' # Сервер, к которому обращаемся за почтой.
MAIL_PORT = 995

MAIL_LOGIN = u'info@iskcon.tomsk.ru'
MAIL_PASSW = u'HjsGh71Hjs'

PROTOCOL = u'pop3'
PROTOCOL_SSL = u'pop3+ssl'

# INSERT INTO mailbox (username,password,name,maildir,quota,domain,isadmin,isglobaladmin,created) VALUES ("info@iskcon.tomsk.ru","$1$BrYSy/27$Ck1cnbhKd9VoP/kvT.76u.","info","iskcon.tomsk.ru/info/",100, "iskcon.tomsk.ru", 1, 1, NOW());
# INSERT INTO alias (address,goto,domain,created) VALUES ("info@iskcon.tomsk.ru", "info@iskcon.tomsk.ru", "iskcon.tomsk.ru", NOW());