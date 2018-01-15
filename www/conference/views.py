# -*- coding: utf-8 -*-

from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings
from django.db.models import Q
from django.db import connections
import urllib
import hashlib
import datetime
import string
import random
import re, os

try:
    import json
except:
    import simplejson as json

from annoying.decorators import render_to
from annoying.utils import HttpResponseReload

from threadmail import threading_simple_send_mail
from conference.models import Category, Group, GroupUserRel, Message,\
    MessageRecipientRel, MessageRequest
from conference.forms import MessageRequestForm, MessageForm,\
    MessageFileFormSet, GroupConfigForm, CauseForm
from conference.email import delete_email
from conference.conf import *


def randstring(n):
    a = string.ascii_letters + string.digits
    return ''.join([random.choice(a) for i in range(n)])

###############################################################################
###############################################################################

###############################################################################
###############################################################################

def custom_proc(request):

    q = Q(group__is_active=True) & (
        Q(group__users=request.user) | Q(group__leaders=request.user) | 
        Q(group__perm__in=[10, 15, 20])
    )
    if not request.user.conference_profile.is_trusted:
        q = q & Q(group__is_visibility_all_users=True)

    return {
        'category_list': Category.activs.filter(q).distinct(),
        'profile_nav': 6,
    }
    
###############################################################################
###############################################################################

###############################################################################
###############################################################################

@login_required
def index(request):
    u"""
    Главная страница приложения - список категорий/групп + инструкция
    
    """

    #Только для лидеров и/или админов. Список запросов пользователей. 
    q = Q(group__leaders=request.user)
    if request.user.is_superuser:
        q = q | Q(group__isnull=True)
    user_requests_list = MessageRequest.objects.filter(q).distinct()
    
    #Только для лидеров и/или админов. #Список сообщений для модерации.
    moderate_messages_list = Message.objects.filter(q).filter(
        is_moderate=False
    ).distinct()
    
    #Группы и их последнии сообщения на главной странице приложения.
    user_group_list = Group.activs.filter( 
        Q(users=request.user, groupuserrel__is_frozen=False,
          groupuserrel__is_active=True) | Q(leaders=request.user)
    ).distinct()
    
    return render_to_response('conference/index.html', {
        'user_requests_list': user_requests_list,
        'moderate_messages_list': moderate_messages_list,
        'user_group_list': user_group_list,
        'cause_form': CauseForm(),
    }, RequestContext(request, processors=[custom_proc]))
    
###############################################################################
###############################################################################

@login_required
def group_user_list(request):
    u"""
    Возвращает список участников группы.
    
    """
    error_msg = u'Не удалось загрузить данные. Повторите попытку.'
    
    try:
        group_id = int(
            request.GET.get('group_id', 0) or 0
        )
        group = Group.objects.get(id=group_id, is_active=True)
    except:
        return HttpResponse(error_msg)
        
    is_staff = group.is_staff(request.user)
    
    if group.is_public_user_list or is_staff:
        user_list = group.get_user_list(request.user)
        
        return HttpResponse(
            render_to_string(
                'conference/group_user_list.html',
                {'group':group, 'user_list':user_list, 'is_staff':is_staff},
                RequestContext(request)
            )
        )

    return HttpResponse(error_msg)
    
###############################################################################
###############################################################################

@login_required
def admin_contact(request):
    u"""
    Написать сообщение админу/лидеру группы
    
    """
    if request.method == 'POST':
    
        group_id = None
        if 'group' in request.GET:
            try:
                group_id = int( request.GET.get('group') )
            except:
                raise Http404('Некорректный идентификатор конференции.')
                
        group = None
        if group_id:
            group = get_object_or_404(Group, id=group_id, is_active=True)
            if not group.is_in_group(request.user):
                raise Http404(u'Вы не можете написать администратору этой '
                              u'конференции.')
                
        obj = MessageRequest(user=request.user, group=group)
        
        form = MessageRequestForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, 'Сообщение отправлено!'
            )
            return HttpResponseRedirect(
                u'%s%s' % (
                    reverse('conference_admin_contact'),
                    (u'?group=%d' % group_id) if group_id else u''
                )
            )
    else:
        form = MessageRequestForm()

    return render_to_response(
        'conference/admin_contact.html', {'form':form},
        RequestContext(request, processors=[custom_proc])
    )

###############################################################################
###############################################################################

@login_required
def admin_contact_del(request, req_id):
    u"""
    Удалить запрос пользователя
    
    """
    req = get_object_or_404(MessageRequest, id=req_id)
    if (
        req.group and req.group.is_staff(request.user)
    ) or request.user.is_superuser:
        req.delete()
        messages.add_message(request, messages.SUCCESS, u'Сообщение успешно '
                                                        u'удалено.')
    else:
        raise Http404()
        
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def admin_moderate_ok(request, msg_id):
    u"""
    Модерация. Одобрить сообщение.
    
    """
    msg = get_object_or_404(Message, id=msg_id)
    if (
        msg.group and msg.group.is_staff(request.user)
    ) or request.user.is_superuser:
        msg.is_moderate = True
        msg.save()
        messages.add_message(request, messages.SUCCESS, 'Сообщение одобрено.')
    else:
        raise Http404()
        
    return HttpResponseReload(request)
    
@login_required
def admin_moderate_del(request, msg_id):
    u"""
    Модерация. Удалить сообщение.
    
    """
    
    msg = get_object_or_404(Message, id=msg_id)
    
    if request.method == 'POST':
        form = CauseForm(request.POST)
        if form.is_valid():
            if (
                msg.group and msg.group.is_staff(request.user)
            ) or request.user.is_superuser:
                msg.delete()
                messages.add_message(
                    request, messages.SUCCESS, 'Сообщение удалено.'
                )
                
                domain = Site.objects.get_current().domain
                email_data = msg.group.get_email_data()
                
                text = form.cleaned_data['text']
                if not text:
                    text = u'Не указана.'
                
                threading_simple_send_mail(
                    'mail/conference_failure.html',
                    u'Отказано в публикации сообщения',
                    [msg.user.email],
                    {
                        'message': u'Причина отказа: %s' % text,
                        'domain':domain, 'sign':email_data['sign']
                    },
                    from_email = email_data['from_email'],
                    connection = email_data['backend'],
                    sender_name = msg.group.get_title(),
                )
            else:
                raise Http404()
            
            return HttpResponseReload(request)
    raise Http404()
    
###############################################################################
###############################################################################

@login_required
def group(request, group_id):
    u"""
    Страница группы. Информация о группе, приглашение вступить или сообщения 
    группы.
    
    """
    obj = get_object_or_404(Group, id=group_id, is_active=True)
    is_in_group = obj.is_in_group(request.user)
    
    form = MessageForm()
    formset = MessageFileFormSet()
    
    parent = None
    form_comment = None
    
    group_config_form_flag = False
    group_config_form = None    
    if obj.is_staff(request.user):
        group_config_form = GroupConfigForm(instance=obj)
        
    if request.method == 'POST':
        group_config_form_flag = bool(
            request.POST.get('group_config_form_flag', False)
        )
        if group_config_form_flag:
            #Если форма настроек группы
            if obj.is_staff(request.user):
                group_config_form = GroupConfigForm(request.POST, instance=obj)
                if group_config_form.is_valid():
                    group_config_form.save()
                    messages.add_message(
                        request, messages.SUCCESS, u'Настройки сохранены.'
                    )
                    return HttpResponseRedirect(
                        reverse('conference_group', kwargs={'group_id':obj.id})
                    )
        else:
            #Если сообщение или комментарий
            if not is_in_group and not obj.has_perm_go_into_group():
                raise Http404()
                
            if obj.is_banned(request.user) or \
               not obj.can_write_message(request.user):
                messages.add_message(
                    request, messages.WARNING, u'Вам запрещено писать '
                                               u'сообщения.'
                )
            elif obj.is_frozen(request.user):
                messages.add_message(
                    request, messages.WARNING, u'Вы заморожены. Вам запрещено '
                                               u'писать сообщения.'
                )
            else:
                is_moderate = False if obj.is_moderate else True
                if obj.is_staff(request.user):
                    #Если сообщение написал лидер или суперпользователь, то 
                    #считаем, что сообщение сразу прошло модерацию.
                    is_moderate = True
                
                instance = Message(
                    group=obj, user=request.user, is_moderate=is_moderate
                )

                form = MessageForm(
                    request.POST, request.FILES, instance=instance
                )
                formset = MessageFileFormSet(
                    request.POST, request.FILES, instance=instance
                )
                
                if form.is_valid() and formset.is_valid():
                    msg = form.save()
                    formset.save()
                
                    for u in obj.get_recipient_list():
                        MessageRecipientRel.objects.create(user=u, message=msg)
                    
                    message_text = u'Сообщение отправлено!'
                    if obj.is_moderate:
                        message_text += u' После проверки модератором оно '\
                                        u'станет доступным для всех '\
                                        u'пользователей.'
                        
                    messages.add_message(
                        request, messages.SUCCESS, message_text
                    )
                    return HttpResponseRedirect(
                        reverse('conference_group', kwargs={'group_id':obj.id})
                    )
    
    return render_to_response('conference/group.html', {
        'group': obj, 
        'is_in_group': is_in_group, 
        'form': form,
        'formset': formset,
        'group_config_form': group_config_form,
        'group_config_form_flag': group_config_form_flag,
    }, RequestContext(request, processors=[custom_proc]))
    
###############################################################################
###############################################################################

@login_required
def group_subscribe(request, group_id):
    u"""
    Подписаться или создать заявку на ступление в группу.
    
    """
    
    obj = get_object_or_404(Group, id=group_id, is_active=True)
    is_in_group = obj.is_in_group(request.user)
    
    if not is_in_group and not obj.has_perm_go_into_group():
        raise Http404()
        
    obj_rel, create = GroupUserRel.objects.get_or_create(
        group=obj, user=request.user
    )
    if not create:
        if obj_rel.is_active:
            messages.add_message(
                request, messages.INFO, u'Вы уже являетесь участником '
                                        u'конференции.'
            )
        else:
            messages.add_message(
                request, messages.INFO, u'Вы уже отправляли заявку на '
                                        u'вступление.'
            )
    else:
        if obj.is_public():
            messages.add_message(
                request, messages.SUCCESS, u'Вы успешно вступили в '
                                           u'конференцию.'
            )
        else:
            obj_rel.is_active = False
            obj_rel.save()
            messages.add_message(
                request, messages.SUCCESS, u'Заявка на вступление отправлена.'
            )
            
            MessageRequest.objects.create(
                group = obj, 
                user = request.user, 
                theme = u'Заявка на вступление в конференцию', 
                text = u'Пользователь %s подал заявку на вступление в '
                       u'конференцию "%s".' % (
                            request.user.get_full_name() if request.user.get_full_name() else request.user.username,
                            obj.get_title(),
                        )
            )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_admin(request, group_id, user_id):
    u"""
    Подписать пользователя, подавшего заявку.
    
    """
    
    group = get_object_or_404(Group, id=group_id, is_active=True)
    is_staff = group.is_staff(request.user)
    if is_staff:
        user = get_object_or_404(User, id=user_id)
        req = group.is_request_in_group(user)
        if req:
            req.is_active = True
            req.save()
            messages.add_message(
                request, messages.SUCCESS, u'Пользователь успешно добавлен в '
                                           u'конференцию.'
            )
        else:
            messages.add_message(
                request, messages.WARNING, u'Не найдена заявка пользователя '
                                           u'на вступление.'
            )
    else:
        messages.add_message(
            request, messages.ERROR, u'У вас недостаточно прав.'
        )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_admin_cancel(request, group_id, user_id):
    u"""
    Отклонить заявку на вступление
    
    """
    
    group = get_object_or_404(Group, id=group_id, is_active=True)
    is_staff = group.is_staff(request.user)
    if is_staff:
        user = get_object_or_404(User, id=user_id)
        req = group.is_request_in_group(user)
        if req:
            req.delete()
            messages.add_message(
                request, messages.SUCCESS, u'Заявка пользователя успешно '
                                           u'отклонена.'
            )
        else:
            messages.add_message(
                request, messages.WARNING, u'Не найдена заявка пользователя '
                                           u'на вступление.'
            )
    else:
        messages.add_message(
            request, messages.ERROR, u'У вас недостаточно прав.'
        )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_del(request, group_id):
    u"""
    Отписаться от группы.
    
    """
    
    obj = get_object_or_404(
        GroupUserRel, group_id=group_id, user=request.user, is_active=True
    )
    obj.delete()
    
    messages.add_message(
        request, messages.SUCCESS, u'Вы успешно отписались от конференции.'
    )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_admin_del(request, group_id, user_id):
    u"""
    Отписать пользователя от группы.
    
    """
    
    group = get_object_or_404(Group, id=group_id, is_active=True)
    is_staff = group.is_staff(request.user)
    if is_staff:
        user = get_object_or_404(User, id=user_id)
        obj = group.get_user_subscribe(user)
        if obj:
            obj.delete()
            messages.add_message(
                request, messages.SUCCESS, u'Пользователь успешно отписан от '
                                           u'конференции.'
            )
        else:
            messages.add_message(
                request, messages.WARNING, u'Пользователь не является '
                                           u'участником конференции.'
            )
    else:
        messages.add_message(
            request, messages.ERROR, u'У вас недостаточно прав.'
        )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_frozen(request, group_id):
    u"""
    Заморозить группу.
    
    """
    
    obj = get_object_or_404(
        GroupUserRel, group_id=group_id, user=request.user, is_frozen=False,
        is_active=True
    )
    obj.is_frozen = True
    obj.save()
    
    messages.add_message(request, messages.SUCCESS, u'Конференция заморожена.')
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
def group_subscribe_frozen_del(request, group_id):
    u"""
    Разморозить группу.
    
    """
    
    obj = get_object_or_404(
        GroupUserRel, group_id=group_id, user=request.user, is_frozen=True,
        is_active=True
    )
    obj.is_frozen = False
    obj.save()
    
    messages.add_message(
        request, messages.SUCCESS, u'Конференция разморожена.'
    )
    
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

@login_required
@csrf_exempt
def ban(request, group_id, user_id):
    u"""
    Забанить пользователя на кол-во дней.
    
    """

    value = request.POST.get('value', u'')
    if value:
        try:
            dt = datetime.datetime.strptime( value, u'%d.%m.%Y' )
        except:
            data = json.dumps(
                {'success':False, 'msg':u'Некорректное значение. Укажите дату '
                                        u'в формате "дд.мм.гггг".'}
            )
            return HttpResponse(data)
    else:
        dt = datetime.datetime.now()
        
    group = get_object_or_404(Group, id=group_id, is_active=True)
    is_staff = group.is_staff(request.user)
    if is_staff:
        user = get_object_or_404(User, id=user_id, is_active=True)
        if user == request.user:
            data = json.dumps({
                'success':False, 'msg':u'Нельзя заблокировать себя.'
            })
            return HttpResponse(data)
        if group.ban(user, dt):
            data = json.dumps({'success':True})
            return HttpResponse(data)
        data = json.dumps({
            'success':False, 'msg':u'Произошла ошибка. Повторите попытку '
                                   u'позже.'
        })
        return HttpResponse(data)
        
    data = json.dumps({'success':False, 'msg':u'У вас недостаточно прав.'})
    return HttpResponse(data)
    
###############################################################################
###############################################################################
    
@login_required
@csrf_exempt
def ban_del(request, group_id, user_id):
    u"""
    Удалить бан пользователя.
    
    """
    group = get_object_or_404(Group, id=group_id, is_active=True)
    is_staff = group.is_staff(request.user)
    if is_staff:
        user = get_object_or_404(User, id=user_id, is_active=True)
        if group.ban(user, datetime.datetime.now()):
            messages.add_message(
                request, messages.SUCCESS, u'Пользователь успешно '
                                           u'разблокирован.'
            )
        else:
            messages.add_message(
                request, messages.WARNING, u'Пользователь не заблокирован.'
            )
    else:
        messages.add_message(
            request, messages.ERROR, u'У вас недостаточно прав.'
        )
    return HttpResponseReload(request)
    
###############################################################################
###############################################################################

###############################################################################
###############################################################################

@login_required
@csrf_exempt
def create_email(request):
    value = request.POST.get('value', u'')
    
    if not value:
        data = json.dumps({'success':False, 'msg':u'Некорректное имя.'})
        return HttpResponse(data)
        
    if not re.match(u'^[0-9a-zA-Z_\-]{1,100}$', value):
        data = json.dumps({
            'success':False, 'msg':u'Некорректное имя. Имя должно содержать '
                                   u'только латинские символы, цифры и '
                                   u'символы _-'
        })
        return HttpResponse(data)
        
    login = u'%s@%s' % (value, MAIL_DOMAIN)
    
    cursor = connections[DB_MAIL_NAME].cursor()
    error_msg = u'Произошла ошибка. Повторите попытку позже.'
    
    try:
        cursor.execute(
            "SELECT COUNT(*) FROM `mailbox` WHERE `username`=%s;", [login]
        )
        row = cursor.fetchone()[0] or 0
    except:
        data = json.dumps({'success':False, 'msg':error_msg})
        return HttpResponse(data)
        
    if row != 0  or login in MAIL_EXLUDE_LOGIN:
        data = json.dumps({
            'success':False, 'msg':u'Пользователь с таким именем уже '
                                   u'зарегистрирован.'
        })
        return HttpResponse(data)
        
    passw = randstring(10)
    hash_passwd = os.popen("openssl passwd -1 %s" % passw).read().strip() #Только Linux
    
    uc = request.user.conference_profile
    
    #Удаляем старый e-mail.
    if uc.is_server_email():
        if delete_email( uc.get_full_server_email() ):
            uc.server_email_login = u''
            uc.server_email_passw = u''
            uc.save()
    
    #Регистрируем новый e-mail.
    try:
        cursor.execute(
            "INSERT INTO `mailbox` (username, password, name, domain, maildir) VALUES (%s, %s, %s, %s, %s);",
            [
                login,
                hash_passwd,
                value,
                MAIL_DOMAIN,
                u'%s/%s/' % (MAIL_DOMAIN, value)
            ]
        )
        cursor.execute(
            "INSERT INTO `alias` (address, goto, domain, created, active) VALUES (%s, %s, %s, NOW(), 1);",
            [login, login, MAIL_DOMAIN]
        )
        cursor.connection.commit()
    except:
        data = json.dumps({'success':False, 'msg':error_msg})
        return HttpResponse(data)
    
    request.user.email = login
    request.user.save()
    
    uc.server_email_login = value
    uc.server_email_passw = passw
    uc.save()
    
    data = json.dumps({'success':True})
    return HttpResponse(data)

###############################################################################
###############################################################################

###############################################################################
###############################################################################