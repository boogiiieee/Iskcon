# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from sorl.thumbnail.admin import AdminImageMixin
from sorl.thumbnail.shortcuts import get_thumbnail, delete
from django.contrib.auth.models import User, Group


from iskcon.models import UserProfile, Order
from iskcon.forms import GroupAdminForm, UserAdminForm
from conference.models import ConferenceProfile

##########################################################################
##########################################################################

class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    search_fields = ('name',)
    ordering = ('name',)
 
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)

##########################################################################
##########################################################################

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    
class ConferenceProfileInline(admin.StackedInline):
    model = ConferenceProfile

class UserAdmin(UserAdmin):
    inlines = [UserProfileInline, ConferenceProfileInline]
    form = UserAdminForm
    filter_horizontal = ('groups',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions', 'groups')}),
    )
 
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

##########################################################################
##########################################################################

##############################################################################################
##############################################################################################

#Заказы пользователя    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('get_name_user_admin', 'get_info_user_admin', 'get_order_cost_admin', 'status', 'get_link_order_admin', 'get_order_image_admin',)
    list_filter = ('status',)
    readonly_fields = ('get_name_user_admin', 'get_info_user_admin', 'get_phone_user_admin', 'get_email_user_admin', 'get_link_order_admin', 'get_order_image_admin', 'get_order_cost_admin' )
    fieldsets = (
        (None, {'fields': ('get_name_user_admin', 'get_phone_user_admin', 'get_email_user_admin', 'get_link_order_admin', 'get_order_image_admin', 'get_order_cost_admin', 'status', 'comment')},),
    )
    def get_readonly_fields(self, request, obj=None):
        if obj.status==u'Выдан':
            return ('get_name_user_admin', 'get_phone_user_admin', 'get_email_user_admin', 'get_link_order_admin', 'get_order_image_admin', 'get_order_cost_admin', 'status', 'comment')
        else:
            return super(OrderAdmin, self).get_readonly_fields(request, obj)
    
    def get_name_user_admin(self, obj):
        return u'<strong>%s</strong>' % obj.get_user_name()
    get_name_user_admin.short_description = u'Имя пользователя'
    get_name_user_admin.allow_tags = True
    
    def get_info_user_admin(self, obj):
        return u'<strong>Телефон</strong> - %s<br/><strong>Email</strong> - %s' % (obj.get_user_phone(), obj.get_user_email())
    get_info_user_admin.short_description = u'Инфо пользователя'
    get_info_user_admin.allow_tags = True
    
    def get_phone_user_admin(self, obj):
        return u'<strong>%s</strong>' % obj.get_user_phone()
    get_phone_user_admin.short_description = u'Телефон пользователя'
    get_phone_user_admin.allow_tags = True

    def get_email_user_admin(self, obj):
        return u'<strong>%s</strong>' % obj.get_user_email()
    get_email_user_admin.short_description = u'Email пользователя'
    get_email_user_admin.allow_tags = True
    
    def get_order_cost_admin(self, obj):
        return u'<strong>%s руб.</strong>' % obj.get_cost()
    get_order_cost_admin.short_description = u'Стоимость'
    get_order_cost_admin.allow_tags = True

    def get_order_image_admin(self, obj):
        html = u'<img src="/media/img/no_image_min.png" title="%s" />' % obj.product.title
        if obj.product.image:
            try:
                f = get_thumbnail(obj.product.image, '130x130', quality=99, format='PNG')
                html = '<a href="%s" target="_blank"><img src="%s" title="%s" /></a>' % (obj.product.image.url, f.url, obj.product.title)
            except:pass
        return u'%s' % html
    
    get_order_image_admin.short_description = u'Изображение заказа'
    get_order_image_admin.allow_tags = True
    
    def get_link_order_admin(self, obj):
        return u'<a href="%s" target="_blank">%s</a>' % (obj.get_product_url(), obj.product.get_title())
    get_link_order_admin.short_description = u'Ссылка на товар на сайте'
    get_link_order_admin.allow_tags = True

admin.site.register(Order, OrderAdmin)
