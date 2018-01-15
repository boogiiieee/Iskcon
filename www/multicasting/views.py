# -*- coding: utf-8 -*-

from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
import datetime
from datetime import timedelta

from threadmail import threading_send_mail

from annoying.decorators import render_to
from annoying.functions import get_object_or_None

from multicasting.models import MessagesMulticasting, GroupPermMulticasting, RecipientMulticasting
from multicasting.forms import AddMessagesMulticastingForm


################################################################################################################
################################################################################################################

@login_required
def inbox(request):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	objs = RecipientMulticasting.activs.filter(user = request.user)
	date_now_1 = datetime.datetime.now()- timedelta(days=1)
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'multicasting/inbox.html',
		template_object_name = 'items',
		extra_context = {
			'profile_nav':6,
			'profile_ls':2,
			'date_now_1':date_now_1
		},
	)
	
@login_required	
@render_to('multicasting/inbox_item.html')
def inbox_item(request, id):
	try: item = RecipientMulticasting.activs.get(id = id, user = request.user)
	except:	raise Http404()
	else:
		item.is_new = False
		item.save()
	date_now_1 = datetime.datetime.now()- timedelta(days=1)	
	return {
		'item': item,
		'profile_nav':6,
		'profile_ls':2,
		'date_now_1':date_now_1
	}
	
@login_required	
def inbox_item_delete(request, id):
	try:
		obj = RecipientMulticasting.activs.get(id=id, user=request.user, )
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка удаления сообщения! Обратитесь к администратору.')
	else:
		obj.is_active = False
		obj.save()
		messages.add_message(request, messages.INFO, 'Сообщение успешно удалено.')
		
	return HttpResponseRedirect(
		reverse('multicasting_url', args=[])
	)
	
@login_required
def outbox(request):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	objs = MessagesMulticasting.activs.filter(user = request.user)
	date_now_1 = datetime.datetime.now()- timedelta(days=1)
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'multicasting/outbox.html',
		template_object_name = 'items',
		extra_context = {
			'profile_nav':6,
			'profile_ls':3,
			'date_now_1':date_now_1
		},
	)
	
@login_required
@render_to('multicasting/outbox_item.html')
def outbox_item(request, id):
	try: item = MessagesMulticasting.activs.get(id = id, user = request.user)
	except:	raise Http404()
	date_now_1 = datetime.datetime.now()- timedelta(days=1)	
	return {
		'item': item,
		'profile_nav':6,
		'profile_ls':3,
		'date_now_1':date_now_1
	}
	
@login_required	
def outbox_item_delete(request, id):
	try:
		obj = MessagesMulticasting.activs.get(id=id, user=request.user, )
	except:
		messages.add_message(request, messages.ERROR, 'Ошибка удаления сообщения! Обратитесь к администратору.')
	else:
		obj.is_active = False
		obj.save()
		messages.add_message(request, messages.INFO, 'Сообщение успешно удалено.')
		
	return HttpResponseRedirect(
		reverse('multicasting_outbox_url', args=[])
	)

	
	
@login_required
@render_to('multicasting/add.html')
def add(request):
	u = request.user
	if u.get_profile().is_send_ls:
		current_site = Site.objects.get_current()
		domain = current_site.domain

		if request.GET and request.GET['id']:
			mes = MessagesMulticasting.objects.get(id = int(request.GET['id']))
			theme = mes.theme
			obj = MessagesMulticasting(user=u, theme = theme)
		else:
			obj = MessagesMulticasting(user=u)

		form = AddMessagesMulticastingForm(u, request.POST or None, request.FILES or None, instance=obj)
		if form.is_valid() and request.POST.getlist('recipient'):
			f = form.save(commit=False)
			f.save()
			r_l = []
			for i in request.POST.getlist('recipient'): 
				if i in r_l:pass
				else:
					u_r = User.objects.get(id = int(i))
					recipient = RecipientMulticasting(user=u_r, sms=obj)
					recipient.save()
					r_l.append(i)
					if u_r.email and u_r.get_profile().is_email:
						threading_send_mail('mail/multicasting/create_msg.html', u'Вам пришло личное сообщение на сайте %s' % domain, [u_r.email,], {'obj':recipient, 'domain':domain})
			messages.add_message(request, messages.SUCCESS, u'Сообщение отправлено.')
			form = AddMessagesMulticastingForm(u,)
		else:
			if form.is_valid() and not request.POST.getlist('recipient'):
				messages.add_message(request, messages.ERROR, u'Выберите получателя сообщения.')
		return {
			'form': form,
			'profile_nav':6,
			'profile_ls':1,
		}
	else:
		messages.add_message(request, messages.ERROR, u'Недостаточно прав для отправки сообщения! Обратитесь к администратору или лидеру группы!')
	return {
		'profile_nav':6,
		'profile_ls':1,
	}
		
	
@login_required	
def perm(request):
	try: page = int(request.GET.get('page', 1))
	except: page = 1
	
	group = request.user.leader_group_perm_rel.filter(is_active=True)
	objs = User.objects.filter(user_group_perm_rel__in = group).distinct().order_by('first_name', 'last_name', 'id')
		
	return object_list(request,
		queryset = objs,
		paginate_by = settings.PAGINATE_BY,
		page = page,
		template_name = 'multicasting/perm.html',
		template_object_name = 'items',
		extra_context = {
			'profile_nav':6,
			'profile_ls':4,
		},
	)
	
@login_required	
def perm_no_send(request, id):
	group = request.user.leader_group_perm_rel.filter(is_active=True)
	try:
		u = User.objects.get(id=int(id))
	except:
		messages.add_message(request, messages.ERROR, u'Ошибка изменения прав пользователя! Обратитесь к администратору.')
	else:
		if u.user_group_perm_rel.filter(id__in = group):
			u.get_profile().is_send_ls = False
			u.get_profile().save()
			messages.add_message(request, messages.SUCCESS, u'Пользователю %s успешно приостановлено право рассылки ЛС!' % u.get_full_name())
			if u.email and u.get_profile().is_email:
				current_site = Site.objects.get_current()
				domain = current_site.domain
				threading_send_mail('mail/multicasting/create_msg_perm_no_send.html', u'Вам запретили отправлять личные сообщения на сайте %s' % domain, [u.email,], {'obj':u, 'domain':domain})
		else:
			messages.add_message(request, messages.ERROR, u'Недостаточно прав для изменения прав другого пользователя! Обратитесь к администратору.')
		
	return HttpResponseRedirect(
		reverse('multicasting_perm_url', args=[])
	)
	
@login_required	
def perm_yes_send(request, id):
	group = request.user.leader_group_perm_rel.filter(is_active=True)
	try:
		u = User.objects.get(id=int(id))
	except:
		messages.add_message(request, messages.ERROR, u'Ошибка изменения прав пользователя! Обратитесь к администратору.')
	else:
		if u.user_group_perm_rel.filter(id__in = group):
			u.get_profile().is_send_ls = True
			u.get_profile().save()
			messages.add_message(request, messages.SUCCESS, u'Пользователю %s успешно добавлено право рассылки ЛС!' % u.get_full_name())
			if u.email and u.get_profile().is_email:
				current_site = Site.objects.get_current()
				domain = current_site.domain
				threading_send_mail('mail/multicasting/create_msg_perm_yes_send.html', u'Вам разрешено отправлять личные сообщения на сайте %s' % domain, [u.email,], {'obj':u, 'domain':domain})
		else:
			messages.add_message(request, messages.ERROR, u'Недостаточно прав для изменения прав другого пользователя! Обратитесь к администратору.')
		
	return HttpResponseRedirect(
		reverse('multicasting_perm_url', args=[])
	)

################################################################################################################
################################################################################################################


