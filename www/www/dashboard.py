# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from admin_tools.menu import items, Menu

from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from admin_tools.utils import get_admin_site_name

class CustomMenuDashboard(Menu):
	def init_with_context(self, context):
		site_name = get_admin_site_name(context)

		self.children += [
			items.MenuItem(u'Панель управления', reverse('%s:index' % site_name)),
			
			items.AppList(
				u'Приложения',
				exclude=(
					'django.contrib.*',
				)
			),
			
			items.MenuItem(u'Администрирование',
				children=[
					items.MenuItem(u'Группы', '/admin/auth/group/', enabled=context['request'].user.has_perm("auth.change_group")),
					items.MenuItem(u'Пользователи', '/admin/auth/user/', enabled=context['request'].user.has_perm("auth.change_user")),
					items.MenuItem(u'Сайты', '/admin/sites/site/', enabled=context['request'].user.has_perm("sites.change_site")),
					items.MenuItem(u'Настройки', '/admin/configuration/configmodel/', enabled=context['request'].user.has_perm("configuration.change_configmodel")),
					
				],
			),
			
			items.Bookmarks(),

			items.MenuItem(u'Система заявок', 'http://web-aspect.ru/helpdesk/'),
		]

class CustomIndexDashboard(Dashboard):
	"""
	Custom index dashboard for www.
	"""
	def init_with_context(self, context):
		site_name = get_admin_site_name(context)
		
		user = context['request'].user
		
		group_children = []
		
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/1/'])
		if user.has_perm("article.change_articleitem"): item_children.append([u'Статьи', '/admin/article/articleitem/'])
		if user.has_perm("news.change_newsarticle"): item_children.append([u'Новости', '/admin/news/newsarticle/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Главная', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/3/'])
		if user.has_perm("news.change_newsarticle"): item_children.append([u'Новости', '/admin/news/newsarticle/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Новости', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/2/'])
		if user.has_perm("article.change_articleitem"): item_children.append([u'Статьи', '/admin/article/articleitem/'])
		if user.has_perm("article.change_categoryarticle"): item_children.append([u'Категории статей', '/admin/article/categoryarticle/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Статьи', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/4/'])
		if user.has_perm("article.change_categoryfoto"): item_children.append([u'Категории фото', '/admin/media_content/categoryfoto/'])
		if user.has_perm("article.change_fotoitem"): item_children.append([u'Фото', '/admin/media_content/fotoitem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Фото', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/7/'])
		if user.has_perm("article.change_categoryvideo"): item_children.append([u'Категории видео', '/admin/media_content/categoryvideo/'])
		if user.has_perm("article.change_videoitem"): item_children.append([u'Видео', '/admin/media_content/videoitem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Видео', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/8/'])
		if user.has_perm("article.change_categoryaudio"): item_children.append([u'Категории аудио', '/admin/media_content/categoryaudio/'])
		if user.has_perm("article.change_audioitem"): item_children.append([u'Аудио', '/admin/media_content/audioitem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Аудио', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/9/'])
		if user.has_perm("forum.change_subscription"): item_children.append([u'Подписки', '/admin/forum/subscription/'])
		if user.has_perm("forum.change_attachfile"): item_children.append([u'Прикрепленные файлы', '/admin/forum/attachfile/'])
		if user.has_perm("forum.change_post"): item_children.append([u'Сообщения', '/admin/forum/post/'])
		if user.has_perm("forum.change_thread"): item_children.append([u'Темы', '/admin/forum/thread/'])
		if user.has_perm("forum.change_forum"): item_children.append([u'Форум', '/admin/forum/forum/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Форум', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/6/'])
		if user.has_perm("feedback.change_feedbackitem"): item_children.append([u'Сообщения обратной связи', '/admin/feedback/feedbackitem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Контакты', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/10/'])
		if user.has_perm("adboard.change_categoryadboard"): item_children.append([u'Категории объявлений', '/admin/adboard/categoryadboard/'])
		if user.has_perm("adboard.change_adboarditem"): item_children.append([u'Объявления', '/admin/adboard/adboarditem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Доска объявлений', children=item_children)
			)
			
		item_children = []
		if user.has_perm("my_flatpages.change_flatpage"): item_children.append([u'Текст', '/admin/my_flatpages/flatpage/19/'])
		if user.has_perm("electronic_catalog.change_categoryelectroniccatalog"): item_children.append([u'Категории электронного каталога', '/admin/electronic_catalog/categoryelectroniccatalog/'])
		if user.has_perm("electronic_catalog.change_electroniccatalogitem"): item_children.append([u'Объявления электронного каталога', '/admin/electronic_catalog/electroniccatalogitem/'])
		if item_children:
			group_children.append(
				modules.LinkList(title=u'Электронный каталог', children=item_children)
			)
		
		if group_children:
			self.children.append(modules.Group(
				title=u'Разделы сайта',
				display="tabs",
				children=group_children,
			))
		
		# append a link list module for "quick links"
		self.children.append(modules.LinkList(
			_('Quick links'),
			layout='inline',
			draggable=False,
			deletable=False,
			collapsible=False,
			children=[
				[_('Return to site'), '/'],
				[_('Change password'),
				reverse('%s:password_change' % site_name)],
				[_('Log out'), reverse('%s:logout' % site_name)],
			]
		))

		# append a recent actions module
		self.children.append(modules.RecentActions(_('Recent Actions'), 5))


class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for www.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(_(self.app_title), self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        return super(CustomAppIndexDashboard, self).init_with_context(context)
