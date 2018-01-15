# -*- coding: utf-8 -*-

from django.template.base import Node, NodeList, Template, Context, Variable
from django import template
import re

from article.models import ArticleItem

register = template.Library()

#######################################################################################################################
#######################################################################################################################

#Список статей в контекст
class GetArticleListNode(Node):
	def __init__(self, auth):
		self.auth = auth
		
	def render(self, context):
		if self.auth:
			context['aticle_list'] = ArticleItem.activs.all()[:10]
		else:
			context['aticle_list'] = ArticleItem.publicas.all()[:10]
		return ''
		
def get_aticle_list(parser, token):
	bits = list(token.split_contents())
	if len(bits) != 2:
		raise TemplateSyntaxError(u'Ошибка в шаблонном теге "GetArticleList"')
	return GetArticleListNode(bits[1])
	
get_aticle_list = register.tag(get_aticle_list)

#######################################################################################################################
#######################################################################################################################