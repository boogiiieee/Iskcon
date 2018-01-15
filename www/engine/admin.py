# -*- coding: utf-8 -*-

from django.contrib import admin
import pickle
import datetime

from mptt.admin import MPTTModelAdmin, MPTTChangeList
from django.contrib.admin.views.main import ChangeList
from django.contrib.admin.options import IncorrectLookupParameters
from django.core.paginator import InvalidPage

################################################################################################################
################################################################################################################
#для правильной работы пагинатора
MAX_SHOW_ALL_ALLOWED = 50

class MyChangeList(ChangeList):
    def get_results(self, request):
        paginator = self.model_admin.get_paginator(request, self.query_set, self.list_per_page)
        # Get the number of objects, with admin filters applied.
        result_count = paginator.count

        # Get the total number of objects, with no admin filters applied.
        # Perform a slight optimization: Check to see whether any filters were
        # given. If not, use paginator.hits to calculate the number of objects,
        # because we've already done paginator.hits and the value is cached.
        if not self.query_set.query.where:
            full_result_count = result_count
        else:
            full_result_count = self.root_query_set.count()

        can_show_all = result_count <= MAX_SHOW_ALL_ALLOWED
        multi_page = result_count > self.list_per_page
        # Get the list of objects to display on this page.
        if (self.show_all and can_show_all) or not multi_page:
            result_list = self.query_set._clone()
        else:
            try:
                result_list = paginator.page(self.page_num+1).object_list
            except InvalidPage:
                raise IncorrectLookupParameters

        self.result_count = result_count
        self.full_result_count = full_result_count
        self.result_list = result_list
        self.can_show_all = can_show_all
        self.multi_page = multi_page
        self.paginator = paginator

	

class ChangeListSaveFilter(MyChangeList):
	def __init__(self, request, model, *args, **kwargs):
		self.params = dict(request.GET.items())
		session_key = 'change_list_get_query_%s' % model._meta.object_name

		if not self.params and session_key in request.session:
			p = pickle.loads(request.session[session_key])
			try:
				if p[2] + datetime.timedelta(hours=1) > datetime.datetime.now():
					self.params, request.GET = p[0], p[1]
			except IndexError:
				request.session.pop(session_key)
		
		request.session[session_key] = pickle.dumps([self.params, request.GET, datetime.datetime.now()])
		super(ChangeListSaveFilter, self).__init__(request, model, *args, **kwargs)
		self.params['all'] = True
	
class ModelAdminSaveFilter(admin.ModelAdmin):
	def get_changelist(self, request, **kwargs):
		return ChangeListSaveFilter

################################################################################################################
################################################################################################################

class MPTTChangeListSaveFilter(MPTTChangeList, ChangeListSaveFilter):
    pass
	
class MPTTAdminSaveFilter(MPTTModelAdmin):
	def get_changelist(self, request, **kwargs):
		# Category.tree.rebuild()
		return MPTTChangeListSaveFilter
