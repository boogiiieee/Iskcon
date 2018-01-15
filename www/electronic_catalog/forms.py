# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User, AnonymousUser
from django.forms.widgets import TextInput
from django.forms.extras import SelectDateWidget
import datetime

from registration.forms import RegistrationForm
from django.contrib.auth.forms import PasswordResetForm
from captcha.fields import CaptchaField

from electronic_catalog.models import ElectronicCatalogItem
from engine.widgets import ImageWidget

##################################################################################################	
##################################################################################################

class AddElectronicCatalogForm(forms.ModelForm):
	class Meta:
		model = ElectronicCatalogItem
		widgets = {
			'image': ImageWidget(attrs={}),
			'text':forms.Textarea(attrs={'rows':"8", 'class':"span12", 'required':True}), 
			'title': forms.TextInput(attrs={'class':"span4", 'required':True }),
			'cost': forms.TextInput(attrs={'class':"span4", 'required':True }),
		}
		fields = ('title', 'cost', 'image', 'is_public', 'text')
		
##################################################################################################	
##################################################################################################
