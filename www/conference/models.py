# -*- coding: utf-8 -*-

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.core.mail.backends.smtp import EmailBackend
from django.utils.safestring import mark_safe
from django.utils.encoding import smart_str
from django.conf import settings
import datetime
import os

from redactor.fields import RedactorField
from django_mailbox.models import Mailbox
from private_media.storages import PrivateMediaStorage
from pytils.translit import slugify
from BeautifulSoup import BeautifulSoup
import bleach

from engine.models import ActiveSortModel, DateCreateModel, Title2Model
from configuration.views import get_config
from conference.email import delete_email
from conference.conf import *

###############################################################################
###############################################################################

PERM_CHOICES = [
    (10, u'Общая. Пользователи самостоятельно подписываются и пишут '
         u'сообщения.'),
    (15, u'Общая. Пользователи самостоятельно подписываются, но писать '
         u'сообщения не могут.'),
    (20, u'Закрытая 1. Пользователь подает заявку на участие.'),
    (30, u'Закрытая 2. Пользователи назначаются администратором/лидером.'),
    (40, u'Закрытая 3. Пользователи назначаются администратором/лидером. '
         u'Только администратор/лидер пишет сообщения.'),
]

###############################################################################
###############################################################################

#Профиль пользователя       
class ConferenceProfile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, related_name=u'conference_profile'
    )
    is_trusted = models.BooleanField(
        verbose_name=u'доверенный пользователь', default=False
    )
    dub_email = models.BooleanField(
        verbose_name=u'дублировать рассылку на почту', default=False
    )
    one_email = models.BooleanField(
        verbose_name=u'получать все новые сообщения в одном письме',
        default=False
    )
    server_email_login = models.CharField(
        max_length=100, verbose_name=u'логин e-mail', blank=True,
        help_text=u'Логин e-mail пользователя на почтовом сервере без домена. '
                  u'Например, info.'
    )
    server_email_passw = models.CharField(
        max_length=100, verbose_name=u'пароль e-mail', blank=True,
        help_text=u'Пароль пользователя на почтовом сервере. Генерируется '
                  u'автоматически. Не меняйте его!'
    )
    
    def __unicode__(self):
        return u'%s' % (self.user.get_full_name() or self.user.username,)
 
    class Meta: 
        verbose_name = u'карточка пользователя'
        verbose_name_plural = u'конференции'
        
    @property
    def mail_server_interface(self):
        u"""
        Вернет адрес клиентского сервиса для просмотра и отправки почты.
        
        """
        return MAIL_SERVER_INTERFACE
        
    def get_full_server_email(self):
        u"""
        Вернет полный адрес серверного email.
        
        """
        if self.server_email_login:
            return u'%s@%s' % (self.server_email_login, MAIL_DOMAIN)
        return u''
        
    def is_server_email(self):
        u"""
        Проверяет задан ли серверный e-mail.
        
        """
        email = self.get_full_server_email()
        if email and email == self.user.email:
            return True
        return False

        
def create_user_profile(sender, instance, created, **kwargs):
    u"""
    Создаем профиль при создании пользователя.
    
    """
    profile, created = ConferenceProfile.objects.get_or_create(user=instance)
    
post_save.connect(create_user_profile, sender=User)


def delete_user_profile(sender, instance, *args, **kwargs):
    u"""
    При удалении пользователя удаляем его e-mail.
    
    """
    uc = instance.conference_profile
    delete_email(uc.server_email_login)

pre_delete.connect(delete_user_profile, sender=User)

###############################################################################
###############################################################################

class Ban(DateCreateModel):
    u"""
    Список забаненых пользователей
    
    """
    user = models.OneToOneField(User, verbose_name=u'пользователь')
    date_ban_end = models.DateField(verbose_name=u'дата окончания ограничений')
    
    def __unicode__(self):
        return self.user.username
        
    class Meta: 
        verbose_name = u"ограничение"
        verbose_name_plural = u"ограничения пользователей"
        ordering = ['-id',]

###############################################################################
###############################################################################

class Category(Title2Model): #TitleModel, ActiveSortModel, DateCreateModel
    u"""
    Категории групп
    
    """
    def __unicode__(self):
        return self.get_title()
        
    class Meta: 
        verbose_name = u"категория"
        verbose_name_plural = u"категории"
        ordering = ['sort', 'title']
        
    def get_group_list(self, user):
        u"""
        Возвращает список групп для категории, в которые можно вступить или, 
        в которые уже вступили.
        
        """
        
        q = Q(is_active=True) & (
            Q(perm__in=[10, 15, 20]) | Q(users=user) | Q(leaders=user)
        )
        if not user.conference_profile.is_trusted:
            q = q & Q(is_visibility_all_users=True)
        
        return self.group_set.filter(q).distinct()

###############################################################################
###############################################################################

class Group(Title2Model): #TitleModel, ActiveSortModel, DateCreateModel
    u"""
    Группы
    
    """
    
    category = models.ForeignKey(Category, verbose_name=u'категория')
    perm = models.IntegerField(verbose_name=u'тип', choices=PERM_CHOICES)
    description = RedactorField(max_length=10000, verbose_name=u'описание',
                                blank=True)
    
    users = models.ManyToManyField(
        User, verbose_name=u'пользователи', blank=True,
        related_name='users_group_rel',
        help_text=u'Пользователи могут писать и читать сообщения в пределах '
                  u'конференции', through="GroupUserRel"
    )
    leaders = models.ManyToManyField(
        User, verbose_name=u'лидеры', blank=True,
        related_name='leaders_group_rel',
        help_text=u'Лидер может подписать, заблокировать, отписать '
                  u'пользователя. Лидер модерирует сообщения, добавляет '
                  u'пользователей в рассылку на основании их запросов.'
    )
    
    is_visibility_all_users = models.BooleanField(
        verbose_name=u'видимость всем пользователям', default=False,
        help_text=u'Если "нет", то коференция будет видна только доверенным '
                  u'пользователям.'
    )
    is_visible_members = models.BooleanField(
        verbose_name=u'видны ли участники', default=False
    )
    is_moderate = models.BooleanField(
        verbose_name=u'модерировать сообщения', default=False
    )
    is_moderate_unregistered = models.BooleanField(
        verbose_name=u'Получать e-mail сообщения от пользователй, которые '
                     u'не являются участниками конференции', default=False,
        help_text=u'Сообщения принимаются в том случае, если в конференции '
                  u'разрешено модерирование сообщений. Все подобные сообщения '
                  u'подлежат проверке модератором.'
    )
    is_behalf_author = models.BooleanField(
        verbose_name=u'e-mail рассылка от имени автора сообщения', default=False,
        help_text=u'Если участник конференции настроил получение всех '
                  u'сообщений на e-mail одним письмом, то это письмо всегда '
                  u'будет отправляться с адреса конференции.'
    )
    lifetime = models.IntegerField(
        verbose_name=u'время жизни сообщений, дней', default=0,
        help_text=u'0 - без ограничений'
    )
    
    
    server_email_protocol = models.CharField(
        max_length=100, verbose_name=u'протокол', choices=[
            (PROTOCOL_SSL, PROTOCOL_SSL), (PROTOCOL, PROTOCOL)
        ], default=PROTOCOL_SSL
    )
    server_email_login = models.EmailField(
        max_length=100, verbose_name=u'логин e-mail', blank=True,
        help_text=u'Логин e-mail конференции на почтовом сервере с доменом. '
                  u'Например, info@iskcon.tomsk.ru. '
                  u'ВНИМАНИЕ! Вся почта с этого почтового ящика автоматичски '
                  u'удаляется. Зарегистрировать новый e-mail можно '
                  u'<a href=\"group_create_email/\">здесь</a>.'
                  u'Удалить <a href=\"group_delete_email/\">здесь</a>'
    )
    server_email_passw = models.CharField(
        max_length=100, verbose_name=u'пароль e-mail', blank=True,
        help_text=u'Пароль e-mail конференции на почтовом сервере.'
    )
    server_email_domain = models.CharField(
        max_length=100, verbose_name=u'домен почтового сервера', blank=True,
    )
    server_email_port = models.PositiveIntegerField(
        verbose_name=u'порт почтового сервера', default=MAIL_PORT,
    )
    
    
    email_sign = RedactorField(
        max_length=1000, verbose_name=u'подпись в письме',
        allow_file_upload=False, allow_image_upload=False, blank=True,
        help_text=u'Если это поле не заполнено, то будет использоваться '
                  u'подпись, заданная в настройках сайта.'
    )
    
    def get_description(self):
        return mark_safe(self.description)
        
    def get_email_sign(self):
        return mark_safe(self.email_sign)
    
    def __unicode__(self):
        return self.get_title()
        
    class Meta: 
        verbose_name = u"конференция"
        verbose_name_plural = u"конференции"
        ordering = ['sort', 'title']
        
    def get_cache_key(self, user, prefix=u''):
        u"""
        Ключ для генерации кэша уникального для каждого пользователя.
        
        """
        return u'%s%s-%s' % (prefix, self.pk, user.pk)
        
    def is_public(self):
        u"""
        Возвращает True если группа открытая, иначе False
        
        """
        if self.perm in [10, 15]:
            return True
        return False
        
    def has_perm_go_into_group(self):
        u"""
        Возвращает True если группа открытая или 1ая закрытая, т.е. 
        пользователи могут вступать в группу или могут подавать заявку на 
        вступление
        
        """
        if self.perm in [10, 15, 20]:
            return True
        return False
        
    def is_public_user_list(self):
        u"""
        Отображать ли список участников.
        
        """
        return self.is_visible_members
        
    def get_user_list(self, user=None):
        u"""
        Возвращает список активных участников группы и лидеров если user не 
        админ/лидер. Иначе выборка делается в соответствии с правами user.
        
        """
        if user and self.is_staff(user):
            user_list = self.users.all().values_list('id', flat=True)
        else:
            user_list = self.users.filter(
                groupuserrel__is_active=True
            ).distinct().values_list('id', flat=True)
        
        leaders_list = self.leaders.all().values_list('id', flat=True)
        return User.objects.filter(
            id__in=list(set(list(leaders_list)+list(user_list))),
            is_active=True
        ).order_by('first_name', 'last_name', 'username')
        
    def get_recipient_list(self):
        u"""
        Возвращает список получателей сообщений в группе.
        
        """
        user_list = self.users.filter(
            groupuserrel__is_active=True, groupuserrel__is_frozen=False
        ).distinct().values_list('id', flat=True)
        leaders_list = self.leaders.all().values_list('id', flat=True)
        return User.objects.filter(
            id__in=list(set(list(leaders_list)+list(user_list))),
            is_active=True
        )
    
    def is_request_in_group(self, user):
        u"""
        Возвращает заявку если пользователь подал заявку на вступление, но не
        вступил.
        
        """
        try:
            obj = GroupUserRel.objects.get(group=self, user=user,
                                           is_active=False)
        except:
            return False
        else:
            return obj
        
    def get_user_subscribe(self, user):
        u"""
        Возвращает активную подписку пользователя в группе или False.
        
        """
        try:
            obj = GroupUserRel.activs.get(group=self, user=user)
        except:
            return False
        else:
            return obj
            
    def is_in_group(self, user):
        u"""
        Возвращает True если user участник группы или лидер группы.
        
        """
        if self.is_leader(user):
            return True
            
        obj = self.get_user_subscribe(user)
        if obj:
            return True
            
        return False
        
    def is_frozen(self, user):
        u"""
        Заморожена ли конференция для пользователя user.
        
        """
        if GroupUserRel.activs.filter(
            group=self, user=user, is_frozen=True
        ).exists():
            return True
        return False
        
    def is_banned(self, user):
        u"""
        Забанен ли пользователь user. Предполагается, что пользователь 
        активен и имеет права на группу.
        Сначала проверяем глобальный бан от админа, затем бан от лидера 
        группы.
            
        """
        try:
            obj = Ban.objects.get(
                user=user, date_ban_end__gt=datetime.datetime.now()
            )
        except:
            pass
        else:
            if obj:
                return obj.date_ban_end
                
        try:
            obj = GroupUserRel.objects.get(
                group=self, user=user, date_ban_end__gt=datetime.datetime.now()
            )
        except:
            pass
        else:
            if obj:
                return obj.date_ban_end

        return False
        
    def ban(self, user, dt):
        u"""
        Забанить пользователя user на до даты dt.
            
        """
        obj = self.get_user_subscribe(user=user)
        if obj:
            obj.date_ban_end = dt
            obj.save()
            return obj.date_ban_end

        return False
        
    def is_leader(self, user):
        u"""
        Является ли пользователь user лидером группы.
        
        """
        if User.objects.filter(pk=user.pk, leaders_group_rel=self).exists():
            return True
        return False
        
    def is_staff(self, user):
        u"""
        Является ли пользователь user лидером группы или администратором.
        
        """
        if user.is_superuser or self.is_leader(user):
            return True
        return False
        
    def can_write_message(self, user):
        u"""
        Может ли пользователь писать в группе
        
        """
        if self.perm in [15, 40] and not self.is_staff(user):
            return False
        return True
        
    def get_messages_list(self, user):
        u"""
            Возвращает список сообщений группы, неудаленных пользователем.
            Полученные сообщения помечаются как прочитанные.
            Не проверяем права пользователя, т.к. сообщение создается для
            пользователей из get_user_list, в которой происходит выборка
            активных незамороженных пользователей.
            
        """
        messages_list = Message.objects.filter(
            group=self, is_moderate=True, recipients=user,
            message_recipient_rel__is_removed=False
        ).distinct()
        MessageRecipientRel.objects.filter(
            user=user, message__in=messages_list.values_list('id', flat=True)
        ).update(is_read=True)
        return messages_list
        
    def get_count_new_messages(self, user):
        u"""
        Возвращает кол-во новых сообщений для пользователя user.
        
        """
        return MessageRecipientRel.activs.filter(
            user=user, message__group=self, message__is_moderate=True,
            is_read=False
        ).count()
        
    def get_last_message(self):
        u"""
        Возвращает последнее сообщение группы.
        
        """
        try:
            return self.message_set.filter(is_moderate=True).latest('id')
        except:
            return None
           
           
    def is_has_server_email(self):
        u"""
        Используется ли почтовый сервер.
        
        """
        if self.server_email_login:
            return True
        return False
        
    def is_external_email(self):
        u"""
        Проверяет, зарегистрирован ли ящик на внешнем почтовом сервере.
        
        """
        if self.server_email_domain != MAIL_SERVER:
            return True
        return False
        
    def get_server_email_protocol(self):
        u"""
        Вернет протокол почтового сервера.
        
        """
        return self.server_email_protocol or PROTOCOL_SSL
        
    def is_server_email_ssl(self):
        u"""
        Используется ли ssl.
        
        """
        if self.get_server_email_protocol() == PROTOCOL_SSL:
            return True
        return False
        
    def get_server_email_login(self):
        u"""
        Вернет логин серверного email.
        
        """
        return self.server_email_login or MAIL_LOGIN
        
    def get_server_email_domain(self):
        u"""
        Вернет домен почтового сервера.
        
        """
        return self.server_email_domain or MAIL_SERVER
        
    def get_server_email_passw(self):
        u"""
        Вернет пароль серверного email.
        
        """
        return self.server_email_passw or MAIL_PASSW
        
    def get_server_email_port(self):
        u"""
        Вернет порт почтового сервера.
        
        """
        return self.server_email_port or MAIL_PORT
        
    def get_server_email_title(self):
        u"""
        Вернет название почтового сервера.
        
        """
        return u'%s in %s' % (
            self.get_server_email_login(),
            self.get_server_email_domain(),
        )
        
        
    def get_email_data(self):
        u"""
        Вернет данные для отправки письма от имени группы.
        
        """
        config = get_config()
        
        if not self.is_has_server_email():
            from_email = None
        else:
            from_email = self.get_server_email_login()
        
        sign = self.get_email_sign()
        if not sign:
            sign = config.get_email_sign()          
        
        return {
            'from_email': from_email,
            'sign': sign,
        }
        
def delete_group(sender, instance, *args, **kwargs):
    u"""
    При удалении конференции удаляем ее e-mail.
    
    """
    if instance.is_has_server_email():
        Mailbox.objects.filter(
            name=instance.get_server_email_title(),
        ).update(active=False)
        
        if not instance.is_external_email():
            delete_email(
                instance.get_server_email_login()
            )
        
pre_delete.connect(delete_group, sender=Group)

###############################################################################
###############################################################################

class GroupUserRel(ActiveSortModel, DateCreateModel):
    u"""
    Пользователи группы
    
    """
    
    group = models.ForeignKey(Group, verbose_name=u'конференция')
    user = models.ForeignKey(User, verbose_name=u'пользователь')
    
    is_frozen = models.BooleanField(verbose_name=u'заморожен', default=False)
    date_ban_end = models.DateField(
        verbose_name=u'дата окончания ограничений', blank=True, null=True
    )
    
    def __unicode__(self):
        return (u'#%d' % self.id) if self and self.id else u'Пользователь'
    
    class Meta:
        unique_together = (("group", "user"),)
        verbose_name = u'пользователь-конференция' 
        verbose_name_plural = u'пользователи-конференции'
        ordering = ['user__first_name', 'user__last_name', 'user__username']
        
def update_group_modified(sender, instance, *args, **kwargs):
    u"""
    Обновление modified группы для обновления кэша группы.
    
    """
    instance.group.save()
    
post_save.connect(update_group_modified, sender=GroupUserRel)
pre_delete.connect(update_group_modified, sender=GroupUserRel)
        
###############################################################################
###############################################################################

class Message(DateCreateModel):
    u"""
    Сообщения
    
    """
    group = models.ForeignKey(Group, verbose_name=u'конференция')
    user = models.ForeignKey(
        User, verbose_name=u'отправитель', related_name='user_message_rel'
    )
    recipients = models.ManyToManyField(
        User, verbose_name=u'получатели', through="MessageRecipientRel",
        blank=True, null=True
    )

    theme = models.CharField(max_length=500, verbose_name=u'тема сообщения')
    text = RedactorField(max_length=10000, verbose_name=u'текст сообщения')
    
    is_moderate = models.BooleanField(
        verbose_name=u'одобрено модератором', default=False
    )
    
    def __unicode__(self):
        return u'%s - %s' % (self.user.username, self.theme)
        
    def get_theme(self):
        return self.theme
        
    def get_text(self):
        # text = bleach.clean(
            # self.text, tags=settings.ALLOWED_TAGS,
            # attributes=settings.ALLOWED_ATTRIBUTES,
            # styles=settings.ALLOWED_STYLES
        # )
        soup = BeautifulSoup(self.text) 
        return mark_safe(soup.prettify())
        
    def get_files(self):
        return self.messagefile_set.all()

    class Meta: 
        verbose_name = u'сообщение'
        verbose_name_plural = u'сообщения'
        ordering = ['-id']
        
        
class MessageFile(models.Model):
    u"""
    Файлы сообщения.
    
    """
    def make_upload_path(instance, filename):
        name, extension = os.path.splitext(filename)
        filename = u'%s%s' % (slugify(name), extension)
        return u'upload/conference/message/%d/%s' % (
            instance.message.group.id, filename.lower()
        )
        
    message = models.ForeignKey(Message, verbose_name=u'сообщение')
    file = models.FileField(
        max_length=500, verbose_name=u'файл', upload_to=make_upload_path,
        storage=PrivateMediaStorage()
    )
    
    def get_title(self):
        return os.path.basename(self.file.path)
        
    def __unicode__(self):
        return self.get_title()
        
    class Meta: 
        verbose_name = u'файл сообщения'
        verbose_name_plural = u'файлы сообщений'
        ordering = ['id']
        
###############################################################################
###############################################################################

class MessageRecipientRel(ActiveSortModel, DateCreateModel):
    u"""
    Связь пользователей и сообщений
    
    """
    
    user = models.ForeignKey(
        User, verbose_name=u'получатель', related_name='user_recipient_rel'
    )
    message = models.ForeignKey(
        Message, verbose_name=u'сообщение',
        related_name='message_recipient_rel'
    )
    
    is_read = models.BooleanField(verbose_name=u'прочитано', default=False)
    is_sent_email = models.BooleanField(
        verbose_name=u'отправлено на e-mail', default=False
    )
    is_removed = models.BooleanField(verbose_name=u'удалено', default=False)
        
    def __unicode__(self):
        return u'#%d' % self.id

    class Meta: 
        verbose_name = u'сообщение-пользователь' 
        verbose_name_plural = u'сообщения-пользователи'
        ordering = ['-id',]
        
    def save(self, *args, **kwargs):
        if not self.user.conference_profile.dub_email:
            self.is_sent_email = True
        super(MessageRecipientRel, self).save(*args, **kwargs)

###############################################################################
###############################################################################

class MessageRequest(DateCreateModel):
    u"""
    Заявки пользователей для лидеров и администратора
    
    """
    
    group = models.ForeignKey(
        Group, verbose_name=u'конференция', blank=True, null=True
    )
    user = models.ForeignKey(User, verbose_name=u'отправитель')
    theme = models.CharField(max_length=500, verbose_name=u'тема сообщения')
    text = models.TextField(max_length=10000, verbose_name=u"текст сообщения")
    
    def __unicode__(self):
        return u'%s - %s' % (self.user.username, self.theme)
        
    class Meta: 
        verbose_name = u'заявка'
        verbose_name_plural = u'заявки пользователей'
        ordering = ['-created']

###############################################################################
###############################################################################