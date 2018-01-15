$(document).ready(function() {

	var content_width = {

		init: function init () {

			var self = this;
			self.contentWidth();

		},

		contentWidth: function contentWidth () {

			var header      = $('body header'),
				menu    	= $('.main_menu'),
				breadcrumbs	= $('#breadcrumbs'),
				content		= $('.conference_content'),
				left		= $('.left_menu'),
				span8_class = 'span8',
				fw			= 'full_width';

				$(document).bind('scroll',function(){
					var hOffset = header.height(),
						mOffset = menu.height(),
						lOffset = left.height(),
						bOffset= breadcrumbs.height(),
						top     = $(document).scrollTop(),
						trigger = false;

					var headerNav =  hOffset + mOffset + lOffset + bOffset + 20;
					
					if (headerNav > top) {
						if (content.data(span8_class) !== true) {
							content.addClass(span8_class).data(span8_class,true);
							if (content.data(fw) !== true) {
								content.removeClass(fw).data(fw,true);
							};

						}
					} else {
						if (content.data(span8_class) !== false) {
							content.removeClass(span8_class).data(span8_class,false);
							if (content.data(fw) !== false) {
								content.addClass(fw).data(fw,false);
							};

						}
					};
					
				});

				$(document).trigger('scroll');
				
		}

	};

	content_width.init();
});