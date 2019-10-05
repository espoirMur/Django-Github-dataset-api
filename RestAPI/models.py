# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Actor(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    login = models.CharField(max_length=50, null=False, unique=True)
    avatar = models.URLField(max_length=200)


class Repo(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    name = models.CharField(max_length=50, null=False, unique=True)
    url = models.URLField(max_length=200)


class Event(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    type = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    actor = models.OneToOneField(
        Actor,
        on_delete=models.CASCADE,
    )
    repo = models.OneToOneField(
        Repo,
        on_delete=models.CASCADE,
    )
