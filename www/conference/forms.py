# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from django.forms.models import BaseInlineFormSet
import re

from djangoformsetjs.utils import formset_media_js

from conference.conf import *
from conference.models import ConferenceProfile, Group, Message, MessageFile,\
    MessageRequest

############################################################################### 
###############################################################################

class GroupAdminForm(forms.ModelForm):
    u"""
    Форма конференции в админке.
    
    """
    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        
        if self.instance.pk is None:
            self.fields['server_email_login'].help_text =\
                u'Логин e-mail конференции на почтовом сервере.'
    
    class Meta:
        model = Group

############################################################################### 
###############################################################################

class GroupCreateEmailAdminForm(forms.ModelForm):
    u"""
    Регистрация e-mail конференции в админке.
    
    """
    def __init__(self, *args, **kwargs):
        super(GroupCreateEmailAdminForm, self).__init__(*args, **kwargs)
        self.fields['server_email_login'].help_text = u''
        self.fields['server_email_passw'].help_text = u'Оставьте пустым для '\
                                                      u'%s' % MAIL_SERVER
        
        for field in ['server_email_login', 'server_email_domain']:
            self.fields[field].required = True
        
    class Meta:
        model = Group
        fields = ('server_email_protocol', 'server_email_login', 
                  'server_email_passw', 'server_email_domain', 
                  'server_email_port')
                  
    def clean_server_email_domain(self):
        value = self.cleaned_data['server_email_domain']
        if not re.match(
            u'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}',
            value
        ):
            raise forms.ValidationError(u'Некорректное значение.')
        return value


############################################################################### 
###############################################################################

class MessageRequestForm(forms.ModelForm):
    u"""
    Заявки пользователей для лидеров и администратора
    
    """
    class Meta:
        model = MessageRequest
        widgets = {
            'text':forms.Textarea(
                attrs={'rows':'8', 'class':'span12',
                       'placeholder':u'Текст сообщения'}
            ), 
            'theme': forms.TextInput(
                attrs={'class':'span12', 'placeholder':u'Тема сообщения'}
            ),
        }
        fields = ('theme', 'text')

############################################################################### 
###############################################################################

class MessageForm(forms.ModelForm):
    u"""
    Форма нового сообщения.
    
    """
    class Meta:
        model = Message
        widgets = {
            'text':forms.Textarea(
                attrs={'rows':'3', 'class':'span12 redactor',
                       'placeholder':u'Текст сообщения'}
            ), 
            'theme': forms.TextInput(
                attrs={'class':'span12', 'placeholder':u'Тема сообщения'}
            ),
        }
        fields = ('theme', 'text')
        

class MessageFileForm(forms.ModelForm):
    u"""
    Форма добавления файла в новое сообщение.
    
    """
    class Meta:
        model = MessageFile
        
    class Media(object):
        js = formset_media_js
        
        
class HiddenDeleteBaseInlineFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(HiddenDeleteBaseInlineFormSet, self).add_fields(form, index)
        if self.can_delete:
            form.fields['DELETE'] = forms.BooleanField(
                required=False,
                widget=forms.HiddenInput
            )
            
            
MessageFileFormSet = inlineformset_factory(
    Message, MessageFile, form=MessageFileForm, 
    formset=HiddenDeleteBaseInlineFormSet, extra=1
)

############################################################################### 
###############################################################################

class GroupConfigForm(forms.ModelForm):
    u"""
    Форма настройки группы
    
    """
    class Meta:
        model = Group
        fields = (
            'is_visible_members', 'is_moderate', 'is_moderate_unregistered',
            'is_behalf_author', 'lifetime'
        )
        
    def clean_lifetime(self): 
        data = self.cleaned_data['lifetime']
        if data and data < 0:
            raise forms.ValidationError(
                u'Значение должно быть больше или равное 0.'
            )
        return data

############################################################################### 
###############################################################################

class ConferenceProfileForm(forms.ModelForm):
    u"""
    Форма профайла
    
    """
    class Meta:
        model = ConferenceProfile
        fields = ('dub_email', 'one_email')
        
class ConferenceProfileFormset(
    inlineformset_factory(
        User, ConferenceProfile, form=ConferenceProfileForm, can_delete=False,
        extra=1, max_num=1
    )
):
    pass
    
############################################################################### 
###############################################################################

class CauseForm(forms.Form):
    u"""
    Форма для написания причины отказа модерации.
    
    """
    
    text = forms.CharField(
        label=u'Причина', widget=forms.Textarea(
            attrs={'rows':'3', 'class':'span12',
                   'placeholder':u'Причина отказа'}
        ), required=False)

############################################################################### 
###############################################################################