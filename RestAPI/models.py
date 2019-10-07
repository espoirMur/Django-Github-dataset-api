# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Actor(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    login = models.CharField(max_length=50, null=False, unique=True)
    avatar_url = models.URLField(max_length=200)


class Repo(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True) # should not be auto
    name = models.CharField(max_length=50, null=False)
    url = models.URLField(max_length=200)

# update actor can have many events

class Event(models.Model):
    id = models.IntegerField(primary_key=True, db_index=True)
    type = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(required=True)
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
    )
    repo = models.ForeignKey(
        Repo,
        on_delete=models.CASCADE,
    )
