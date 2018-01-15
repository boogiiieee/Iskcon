# -*- coding: utf-8 -*-
from django.template import loader, RequestContext
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.views.generic.list_detail import object_list
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.conf import settings
from django.core.urlresolvers import reverse
from annoying.decorators import render_to

from threadmail import threading_send_mail

from conference.forms import ConferenceProfileFormset
from feedback.views import feedback_views
from article.models import ArticleItem, CategoryArticle
from iskcon.models import STATUS_ORDER, Order
from iskcon.forms import ProfileForm
from ad_board.models import CategoryAdBoard, AdBoardItem
from ad_board.forms import AddAdBoardForm

from electronic_catalog.models import ElectronicCatalogItem

from conference.conf import MAIL_DOMAIN

from forum.models import Forum, Thread, Post, Subscription


FORUM_PAGINATION = getattr(settings, 'FORUM_PAGINATION', 10)
PAGINATION = getattr(settings, 'PAGINATION', 10)


@render_to('index.html')
def index(request):
    if request.user.is_authenticated():
        cat_menu = CategoryArticle.activs.all()
        objs = ArticleItem.activs.filter(category__in = cat_menu)
    else:
        cat_menu = CategoryArticle.publics.all()
        objs = ArticleItem.publics.filter(category__in = cat_menu)
    
    return object_list( 
        request,
        queryset = objs,
        paginate_by = PAGINATION,
        template_object_name = 'aticle',
        template_name = 'index.html',
        extra_context = {
            'active':1,
        }
    )

def contacts(request):
    return feedback_views(request, 'contacts.html')
    
    
##########################################################################
##########################################################################

@login_required
@render_to('email.html')
def profile_email(request):
    from conference import conf
    server_url = conf.MAIL_SERVER_INTERFACE
    return HttpResponseRedirect(server_url)

##########################################################################
##########################################################################
    
@login_required
def profile_change_password(request):
    if request.method == 'POST':
        form2 = PasswordChangeForm(user=request.user, data=request.POST)
        if form2.is_valid():
            form2.save()
            messages.add_message(request, messages.INFO, 'Пароль успешно изменен.')
            return HttpResponseRedirect('/accounts/profile/')
    messages.add_message(request, messages.ERROR, 'Ошибка изменения пароля!')
    return HttpResponseRedirect('/accounts/profile/')

##########################################################################
##########################################################################

@login_required
def profile_views(request):
    help_text = u''
    uc = request.user.conference_profile
    if uc.is_server_email():
        help_text = u'Сервер %s. Пароль: %s' % (uc.mail_server_interface, uc.server_email_passw)
    
    if request.method == 'POST':
        form1 = ProfileForm(request.POST, request.FILES, instance=request.user)
        formset1 = ConferenceProfileFormset(request.POST, instance=request.user)
        
        if form1.is_valid() and formset1.is_valid():
            form1.save()
            formset1.save()
            messages.add_message(request, messages.INFO, 'Данные сохранены.')
            return HttpResponseRedirect('/accounts/profile/')
    else:
        form1 = ProfileForm(instance=request.user, initial={'last_name':request.user.last_name, 'first_name':request.user.first_name, 'email':request.user.email})
        formset1 = ConferenceProfileFormset(instance=request.user)
        
    form1.fields['email'].help_text = help_text
    form2 = PasswordChangeForm(request.user)

    return render_to_response('profile.html', {'form1':form1, 'formset1':formset1, 'form2':form2, 'profile_nav':1, 'mail_domain':MAIL_DOMAIN}, RequestContext(request))

    
##########################################################################
##########################################################################

#Объявления пользователя
@login_required
def profile_ad(request):
    t = AdBoardItem.activs.filter(user=request.user).order_by('id')
    
    return object_list( 
        request,
        queryset = t,
        paginate_by = PAGINATION,
        template_object_name = 'items',
        template_name = 'ad_board/profile_ads.html',
        extra_context = {
            'profile_nav': 2,
        }
    )
    
#Редактирование Объявления пользователя 
@login_required
@render_to('ad_board/profile_edit_ad.html')
def profile_ad_edit(request, id):
    try:
        id = int(id)
    except TypeError:
        raise Http404()
        
    try:
        obj = AdBoardItem.activs.get(id=id)
    except:
        raise Http404()

    form = AddAdBoardForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, u'Объявление успешно отредактировано.')
        return HttpResponseRedirect(u'%s' % obj.get_profile_ad_url())
    return {
        'form': form,
        'profile_nav':2,
    }
    
#Elfkbnm Объявления пользователя    
@login_required
def profile_ad_delete(request, id):
    try:
        id = int(id)
    except TypeError:
        raise Http404()
        
    try:
        obj = AdBoardItem.activs.get(id=id)
    except:
        messages.add_message(request, messages.ERROR, 'Ошибка удаления убъявления! Обратитесь к администратору.')
    else:
        obj.is_active = False
        obj.save()
        messages.add_message(request, messages.INFO, 'Объявление успешно удалено.')

    return HttpResponseRedirect(
        reverse('profile_ad_url', args=[], kwargs={})
    )
    
##########################################################################
##########################################################################

#Темы в форуме созданные пользователем
@login_required
def profile_thread(request):
    t = Thread.objects.select_related().filter(author=request.user).order_by('id')
    
    return object_list( 
        request,
        queryset = t,
        paginate_by = FORUM_PAGINATION,
        template_object_name = 'thread',
        template_name = 'forum/profile_thread_list.html',
        extra_context = {
            'profile_nav': 4,
        }
    )
    
#Сообщения в форуме созданные пользователем
@login_required
def profile_post(request):
    p = Post.objects.select_related().filter(author=request.user).order_by('time')
    
    return object_list( 
        request,
        queryset = p,
        paginate_by = FORUM_PAGINATION,
        template_object_name = 'post',
        template_name = 'forum/profile_post_list.html',
        extra_context = {
            'profile_nav': 5,
        }
    )

##########################################################################
##########################################################################


#Сделать заказ
@login_required
def order(request, id):
    try:
        p = ElectronicCatalogItem.activs.get(id = id)
    except:
        messages.add_message(request, messages.ERROR, u'Ошибка при оформлении заказа! Обратитесь к администратору или повторите попытку позже!')
    else:
        o = Order.objects.create(user = request.user, product = p, status = STATUS_ORDER[0][0], cost = p.cost)

        current_site = Site.objects.get_current()
        domain = current_site.domain
        
        users = User.objects.filter(is_staff=True, is_active=True)
        emails = [u.email for u in users]
        if emails:
            threading_send_mail('mail/order/create_msg_admin.html', u'Новый заказ на сайте %s' % domain, emails, {'obj':o, 'domain':domain})
        if request.user.email:
            threading_send_mail('mail/order/create_msg.html', u'Ваш заказ на сайте %s принят' % domain, emails, {'obj':o, 'domain':domain})
            
        messages.add_message(request, messages.INFO, u'Спасибо, Ваш заказ создан! За статусом выполнения заказа Вы можете наблюдать в личном кабинете!')

    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    
    
#Заказы пользователя
@login_required
def profile_order(request):
    t = Order.activs.filter(user=request.user)
    
    return object_list( 
        request,
        queryset = t,
        paginate_by = PAGINATION,
        template_object_name = 'items',
        template_name = 'electronic_catalog/profile_orders.html',
        extra_context = {
            'profile_nav': 3,
        }
    )
