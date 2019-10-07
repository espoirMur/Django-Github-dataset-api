# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actor, Event, Repo


# Register your models here.
admin.site.register(Actor)
admin.site.register(Repo)
admin.site.register(Event)
