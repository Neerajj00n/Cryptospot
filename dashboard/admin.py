# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from dashboard.models import *
#from dashboard.models import Dashconfig
# Register your models here.

admin.site.register(Dashconfig)
admin.site.register(Coin_listings)
admin.site.register(Exchange)
admin.site.register(Airdrop)
admin.site.register(Shop)
