# -*- coding: utf-8 -*-

from django.contrib import admin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db import connections
import urllib
import hashlib
import datetime
import string
import random
import re, os

from annoying.functions import get_object_or_None
from annoying.utils import HttpResponseReload
from django_mailbox.models import Mailbox

from conference.email import delete_email
from conference.models import Ban, Category, Group, GroupUserRel, Message,\
    MessageFile, MessageRecipientRel, MessageRequest
from conference.forms import GroupAdminForm, GroupCreateEmailAdminForm
from conference.conf import *

def randstring(n):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for i in range(n)])

###############################################################################
###############################################################################

class BanAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_ban_end', 'modified', 'created')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    list_filter = ('date_ban_end', 'modified', 'created')

admin.site.register(Ban, BanAdmin)

###############################################################################
###############################################################################

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'sort')
    search_fields = ('title',)
    list_filter = ('is_active', 'modified', 'created')
    list_editable = ('is_active', 'sort')

admin.site.register(Category, CategoryAdmin)

###############################################################################
###############################################################################

class GroupUserRelInline(admin.TabularInline):
    model = GroupUserRel
    extra = 0
    raw_id_fields = ['user']
    
class GroupAdmin(admin.ModelAdmin):
    group_create_email_template = 'conference/admin/group_create_email.html'
    group_create_email_form = GroupCreateEmailAdminForm
    form = GroupAdminForm
    
    inlines = [GroupUserRelInline,]
    list_display = (
        'title', 'category', 'perm', 'is_visibility_all_users',
        'is_visible_members', 'lifetime', 'is_active', 'sort'
    )
    search_fields = ('title',)
    list_filter = (
        'category', 'perm', 'is_visibility_all_users', 'is_visible_members',
        'is_active', 'modified', 'created'
    )
    list_editable = ('is_active', 'sort')
    filter_horizontal = ('leaders',)
    readonly_fields = ('server_email_protocol', 'server_email_login', 
                       'server_email_passw', 'server_email_domain', 
                       'server_email_port')
    
    def get_urls(self):
        from django.conf.urls import patterns
        return patterns('',
            (r'^(\d+)/group_create_email/$',
                self.admin_site.admin_view(self.group_create_email)),
            (r'^(\d+)/group_delete_email/$',
                self.admin_site.admin_view(self.group_delete_email)),
        ) + super(GroupAdmin, self).get_urls()
        
    def group_delete_email(self, request, id, form_url=''):
        u"""
        Удалить e-mail на почтовом сервере.
        
        """
        if not self.has_change_permission(request):
            raise PermissionDenied
            
        obj = get_object_or_None(self.queryset(request), pk=id)
        
        if obj and obj.is_has_server_email():
            if not obj.is_external_email():
                delete_email( obj.get_server_email_login() )
                
            Mailbox.objects.filter(
                name=obj.get_server_email_title(),
            ).update(active=False)
            
            obj.server_email_login = u''
            obj.server_email_passw = u''
            obj.server_email_domain = u''
            obj.save()
                
        messages.success(request,
                         u'E-mail на почтовом сервере успешно удален.')
        return HttpResponseReload(request)
        
    @sensitive_post_parameters()
    def group_create_email(self, request, id, form_url=''):
        u"""
        Зарегистрировать e-mail на почтовом сервере.
        
        """
        if not self.has_change_permission(request):
            raise PermissionDenied
            
        obj = get_object_or_404(self.queryset(request), pk=id)
        
        if request.method == 'POST':
            form = self.group_create_email_form(request.POST, instance=obj)
            if form.is_valid():
                cd = form.cleaned_data
                
                protocol = cd.get('server_email_protocol')
                login = cd.get('server_email_login')
                passw = cd.get('server_email_passw')
                domain = cd.get('server_email_domain')
                port = cd.get('server_email_port')
                
                #Удаляем старый e-mail.
                if obj.is_has_server_email():
                    if not obj.is_external_email():
                        delete_email( obj.get_server_email_login() )
                
                    Mailbox.objects.filter(
                        name=obj.get_server_email_title(),
                    ).update(active=False)
    
                    obj.server_email_login = u''
                    obj.server_email_passw = u''
                    obj.server_email_domain = u''
                    obj.save()
                  
                obj.server_email_protocol = protocol
                obj.server_email_login = login
                obj.server_email_passw = passw
                obj.server_email_domain = domain
                obj.server_email_port = port
                
                if domain == MAIL_SERVER:
                    cursor = connections[DB_MAIL_NAME].cursor()
                    error_msg = u'Произошла ошибка. Повторите попытку позже.'
                    
                    try:
                        cursor.execute(
                            "SELECT COUNT(*) FROM `mailbox` WHERE `username`=%s;",
                            [login,]
                        )
                        row = cursor.fetchone()[0] or 0
                    except:
                        messages.error(request, error_msg)
                        return HttpResponseReload(request)
                        
                    if row != 0 or login in MAIL_EXLUDE_LOGIN:
                        messages.error(
                            request, u'Пользователь с таким именем уже '
                                     u'зарегистрирован.'
                        )
                        return HttpResponseReload(request)
                        
                    passw = randstring(10)
                    hash_passwd = os.popen(
                        "openssl passwd -1 %s" % passw
                    ).read().strip() #Только Linux
                    
                    #Регистрируем новый e-mail.
                    try:
                        cursor.execute(
                            "INSERT INTO `mailbox` (username, password, name, domain, maildir) VALUES (%s, %s, %s, %s, %s);",
                            [
                                login,
                                hash_passwd,
                                login.split(u'@')[0],
                                MAIL_DOMAIN,
                                u'%s/%s/' % (MAIL_DOMAIN, login.split(u'@')[0])
                            ]
                        )
                        cursor.execute(
                            "INSERT INTO `alias` (address, goto, domain, created, active) VALUES (%s, %s, %s, NOW(), 1);",
                            [login, login, MAIL_DOMAIN]
                        )
                        cursor.connection.commit()
                    except:
                        messages.error(request, error_msg)
                        return HttpResponseReload(request)
                    
                    obj.server_email_passw = passw
                
                obj.save()
                    
                box = Mailbox.objects.create(
                    name=obj.get_server_email_title(),
                    uri=u'%s,%s,%s,%s,%s' % (
                        obj.get_server_email_protocol(),
                        urllib.quote(obj.get_server_email_login()),
                        obj.get_server_email_passw(),
                        obj.get_server_email_domain(),
                        obj.get_server_email_port(),
                    ),
                )
                    
                messages.success(request, u'E-mail успешно создан!')
                return HttpResponseRedirect('..')
        else:
            form = self.group_create_email_form(initial={
                'server_email_protocol': PROTOCOL_SSL,
                'server_email_domain': MAIL_SERVER, 
                'server_email_port': MAIL_PORT,
            })

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': u'Регистрация E-mail для конференции: %s' % escape(obj),
            'adminForm': adminForm,
            'form_url': mark_safe(form_url),
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': obj,
            'save_as': False,
            'show_save': True,
            'MAIL_SERVER': MAIL_SERVER,
        }
        return TemplateResponse(
            request, [self.group_create_email_template], context,
            current_app=self.admin_site.name
        )

admin.site.register(Group, GroupAdmin)

###############################################################################
###############################################################################
    
class GroupUserRelAdmin(admin.ModelAdmin):
    list_display = (
        'group', 'user', 'is_frozen', 'date_ban_end', 'modified', 'created',
        'is_active', 'sort'
    )
    search_fields = ('group__title',)
    list_filter = (
        'is_frozen', 'date_ban_end', 'is_active', 'modified', 'created',
        'group'
    )
    list_editable = ('is_active', 'sort')
    raw_id_fields = ['group', 'user']

admin.site.register(GroupUserRel, GroupUserRelAdmin)

###############################################################################
###############################################################################

class MessageFileInline(admin.TabularInline):
    model = MessageFile
    extra = 0
    
class MessageAdmin(admin.ModelAdmin):
    inlines = [MessageFileInline,]
    list_display = (
        'theme', 'group', 'user', 'is_moderate', 'modified', 'created'
    )
    search_fields = ('theme',)
    list_filter = ('is_moderate', 'modified', 'created', 'group')

admin.site.register(Message, MessageAdmin)

###############################################################################
###############################################################################
    
class MessageRecipientRelAdmin(admin.ModelAdmin):
    list_display = (
        'message', 'user', 'is_read', 'is_removed', 'modified', 'created',
        'is_active', 'sort'
    )
    search_fields = ('message__theme',)
    list_filter = ('is_read', 'is_removed', 'is_active', 'modified', 'created')
    list_editable = ('is_active', 'sort')

admin.site.register(MessageRecipientRel, MessageRecipientRelAdmin)

###############################################################################
###############################################################################
    
class MessageRequestAdmin(admin.ModelAdmin):
    list_display = ('theme', 'group', 'user', 'modified', 'created')
    search_fields = ('theme',)
    list_filter = ('modified', 'created', 'group')

admin.site.register(MessageRequest, MessageRequestAdmin)

###############################################################################
###############################################################################