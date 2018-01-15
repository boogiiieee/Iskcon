# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
import re

from news.models import NewsArticle

register = template.Library()

################################################################################################################
################################################################################################################

class GetNewsListNode(Node):
	def __init__(self, auth):
		self.auth = auth
		
	def render(self, context):
		if self.auth:
			context['news_list'] = NewsArticle.publics.all()[:5]
		else:
			context['news_list'] = NewsArticle.activs.all()[:5]
		return ''
		
def get_news_list(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 2:
		raise TemplateSyntaxError(u'Ошибка в шаблонном теге "GetNewsList"')
	return GetNewsListNode(bits[1])
	
get_news_list = register.tag(get_news_list)

################################################################################################################
################################################################################################################