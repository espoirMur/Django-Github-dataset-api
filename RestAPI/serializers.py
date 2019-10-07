# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from .models import Event, Actor, Repo


class ActorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    login = serializers.CharField(required=True)
    avatar = serializers.URLField(required=False)

    class Meta:
        model = Actor
        fields = '__all__'


class RepoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(required=True)
    url = serializers.URLField(required=False)

    class Meta:
        model = Repo
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    type = serializers.CharField(required=True)
    created_at = serializers.DateTimeField()
    actor = ActorSerializer(read_only=True, many=False)
    repo = RepoSerializer(read_only=True, many=False)

    class Meta:
        model = Event
        fields = '__all__'
