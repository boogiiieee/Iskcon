# -*- coding: utf-8 -*-

import datetime

from configuration.models import ConfigModel

##################################################################################################	
##################################################################################################

def custom_proc(request):
	conf, create = ConfigModel.objects.get_or_create(id=1)
	return {
		'config': conf,
		'year': datetime.datetime.now().year
	}
	
##################################################################################################	
##################################################################################################