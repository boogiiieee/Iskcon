# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import TextInput
import datetime

from ad_board.models import AdBoardItem
from engine.widgets import ImageWidget

##################################################################################################	
##################################################################################################

class AddAdBoardForm(forms.ModelForm):
	class Meta:
		model = AdBoardItem
		widgets = {
			'image': ImageWidget(attrs={}),
			'text':forms.Textarea(attrs={'rows':"8", 'class':"span12", 'required':True}), 
			'title': forms.TextInput(attrs={'class':"span4", 'required':True }),
			'cost': forms.TextInput(attrs={'class':"span4", 'required':True }),
		}
		fields = ('title', 'cost', 'image', 'is_public', 'text')
		
##################################################################################################	
##################################################################################################
