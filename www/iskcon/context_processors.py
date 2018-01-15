# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.conf import settings

from article.models import CategoryArticle
from media_content.models import CategoryFoto, CategoryVideo, CategoryAudio
from ad_board.models import CategoryAdBoard
from electronic_catalog.models import CategoryElectronicCatalog

##################################################################################################	
##################################################################################################
def custom_proc(request):
	site = ''
	try:
		site = Site.objects.all()[0].name
	except:pass
	if request.user.is_authenticated():
		article_sub_menu = CategoryArticle.activs.all()
		video_sub_menu = CategoryVideo.activs.all()
		media_sub_menu = CategoryFoto.activs.all()
		audio_sub_menu = CategoryAudio.activs.all()
		ad_board_sub_menu = CategoryAdBoard.activs.all()
		electronic_catalog_sub_menu = CategoryElectronicCatalog.activs.all()
		# count_ls = RecipientMulticasting.activs.filter(is_new = True, user = request.user).count()
	else:
		article_sub_menu = CategoryArticle.publics.all()
		video_sub_menu = CategoryVideo.publics.all()
		media_sub_menu = CategoryFoto.publics.all()
		audio_sub_menu = CategoryAudio.publics.all()
		ad_board_sub_menu = CategoryAdBoard.publics.all()
		electronic_catalog_sub_menu = CategoryElectronicCatalog.publics.all()
		count_ls = None

	return {
		'article_sub_menu': article_sub_menu,
		'video_sub_menu': video_sub_menu,
		'media_sub_menu': media_sub_menu,
		'audio_sub_menu': audio_sub_menu,
		'ad_board_sub_menu':ad_board_sub_menu,
		'electronic_catalog_sub_menu':electronic_catalog_sub_menu,
		'site': site,
		# 'count_ls':count_ls,
        
        'PROTOKOL': settings.PROTOKOL,
	}
	
##################################################################################################	
##################################################################################################
