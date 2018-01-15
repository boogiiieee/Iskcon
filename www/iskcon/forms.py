# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserChangeForm
from django.forms.widgets import TextInput
from captcha.fields import CaptchaField, CaptchaTextInput

from engine.widgets import ImageWidget
from iskcon.models import UserProfile

##################################################################################################  
##################################################################################################

class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions')


class UserAdminForm(UserChangeForm):
    class Meta:
        model = User
        
##################################################################################################  
##################################################################################################

#Профиль пользователя
class ProfileForm(forms.ModelForm):
    file = forms.FileField(required=False, label=u'Ваше фото',widget=ImageWidget())
    phone = forms.CharField(max_length=30, label=u'Телефон', required=False, widget=TextInput())
    #is_email = forms.BooleanField(label=u'Получать уведомление на email о ЛС')
    
    def __init__(self, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        try: 
            self.fields['file'].initial = self.instance.get_profile().file
        except: pass
        try: 
            self.fields['phone'].initial = self.instance.get_profile().phone
        except: pass
        # try: 
            # self.fields['is_email'].initial = self.instance.get_profile().is_email
        # except: pass
        
    def save(self, *args, **kw):
        super(ProfileForm, self).save(*args, **kw)
        try: pf = self.instance.get_profile()
        except: pf = UserProfile.objects.get_or_create(user=self.instance)
        else:
            if self.cleaned_data.get('file'):
                pf.file = self.cleaned_data.get('file')
            else:
                pf.file = ''
            if self.cleaned_data.get('phone'):
                pf.phone = self.cleaned_data.get('phone')
            else:
                pf.phone = ''
            # if self.cleaned_data.get('is_email'):
                # pf.is_email = self.cleaned_data.get('is_email')
            # else:
                # pf.is_email = ''
            pf.save()
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone')#, 'is_email')
        widgets = {
            'first_name':TextInput(attrs={'required':True}),
            'last_name':TextInput(attrs={'required':True}),
            'phone':TextInput(),
            'email':TextInput(attrs={'required':True}),
        }
        
##################################################################################################  
##################################################################################################

from registration.forms import RegistrationForm
from registration.models import RegistrationProfile

#Форма регистрации
class MyRegistrationForm(RegistrationForm):
    first_name = forms.CharField(max_length=30, label=u'Имя', required=False, widget=TextInput())
    last_name = forms.CharField(max_length=30, label=u'Фамилия', required=False, widget=TextInput())
    
    def __init__(self, *args, **kw):
        super(MyRegistrationForm, self).__init__(*args, **kw)
        self.fields['username'].label = u'Логин'
    
    def save(self, profile_callback=None):
        new_user = RegistrationProfile.objects.create_inactive_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password1'],
            email=self.cleaned_data['email'],
            profile_callback=profile_callback
        )
        new_user.first_name=self.cleaned_data['first_name']
        new_user.last_name=self.cleaned_data['last_name']
        new_user.save()
        pf = new_user.get_profile()
        pf.save() 

        return new_user

##################################################################################################  
##################################################################################################