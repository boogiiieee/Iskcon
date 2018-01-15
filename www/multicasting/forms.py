# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import TextInput
from django.contrib.auth.models import User
from django.db.models import Max	
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import gettext	
from django.utils.html import escape
from django.forms.widgets import flatatt
from django.utils.encoding import smart_unicode

from multicasting.models import MessagesMulticasting, GroupPermMulticasting

##################################################################################################	
##################################################################################################

class GroupedSelect(forms.Select): 
    def __init__(self, attrs=None, choices=()):
		super(GroupedSelect, self).__init__(attrs)
		self.choices = list(choices)
    def render(self, name, value, attrs=None, choices=()):
		if value is None: value = '' 
		final_attrs = self.build_attrs(attrs, name=name) 
		output = [u'<select%s multiple="multiple">' % flatatt(final_attrs)] 
		str_value = smart_unicode(value)
		for group_label, group in self.choices: 
			if group_label:
				group_label = smart_unicode(group_label) 
				output.append(u'<optgroup label="%s">' % escape(group_label)) 
			n = 0
			for k, v in group:
				option_value = smart_unicode(group[n][v])
				option_label = smart_unicode(User.objects.get(id=int(group[n][v])).get_full_name()) 
				selected_html = (option_value == str_value) and u' selected="selected"' or ''
				output.append(u'<option value="%s"%s>%s</option>' % (escape(option_value), selected_html, escape(option_label)))
				n = n+1
			if group_label:
				output.append(u'</optgroup>') 
		output.append(u'</select>') 
		return mark_safe(u'\n'.join(output))
		

class GroupedChoiceField(forms.ChoiceField):
    def __init__(self, choices=(), required=True, widget=GroupedSelect, label=None, initial=None, help_text=None):
        super(forms.ChoiceField, self).__init__(required, widget, label, initial, help_text)
        self.choices = choices
        
    def clean(self, value):
		"""
		Validates that the input is in self.choices.
		"""
		# value = super(forms.ChoiceField, self).clean(value)
		if value in (None, ''):
			value = u''
			value = smart_unicode(value)
		if value == u'':
			return value
		valid_values = []
		n = 0
		for group_label, group in self.choices:
			for i in group:
				valid_values.append(str(i['id']))
			n = n+1
		if value not in valid_values or value==u'':
			raise ValidationError(gettext(u'Select a valid choice. That choice is not one of the available choices.'))
		return value

class AddMessagesMulticastingForm(forms.ModelForm):
	recipient = GroupedChoiceField(required=True, choices=(), label='Кому')
	def __init__(self, user = None, *args, **kwargs):
		super(AddMessagesMulticastingForm, self).__init__(*args, **kwargs)
		if user:
			mas = []
			if not user.leader_group_perm_rel.all():
				for u in GroupPermMulticasting.objects.filter(user = user):
					mas.append([u.title, list(u.user.filter(is_active = True).exclude(id=user.id).values('username').annotate(id = Max('id')))])
				self.fields['recipient'].choices = mas
			else:
				for u in GroupPermMulticasting.activs.all():
					mas.append([u.title, list(u.user.filter(is_active = True).exclude(id=user.id).values('username').annotate(id = Max('id')))])
				self.fields['recipient'].choices = mas

	class Meta:
		model = MessagesMulticasting
		widgets = {
			'text':forms.Textarea(attrs={'rows':"8", 'class':"span12", 'required':True}), 
			'theme': forms.TextInput(attrs={'class':"span4", 'required':True }),
			'recipient': GroupedSelect(attrs={'class':"span4", 'required':True }),
		}
		fields = ('recipient', 'theme', 'text', 'file', )
		
##################################################################################################	
##################################################################################################
