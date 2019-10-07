# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers
from .models import Event, Actor, Repo
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.db.models import Q


class ActorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    login = serializers.CharField(required=True)
    avatar_url = serializers.URLField(required=False)

    class Meta:
        model = Actor
        fields = '__all__'


class RepoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(required=True)
    url = serializers.URLField(required=False)

    class Meta:
        model = Repo
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    type = serializers.CharField(required=True)
    actor = ActorSerializer(many=False, required=True)
    repo = RepoSerializer(many=False, required=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S",
                                           required=True)

    class Meta:
        model = Event
        fields = '__all__'

    def create(self, validated_data):
        if True:
            data = validated_data
            try:
                Event.objects.get(pk=data.get('id'))
                raise ValidationError({"message": 'event is already there'},
                                      code=HTTP_400_BAD_REQUEST)
            except Event.DoesNotExist:
                actor_data = data.pop('actor')
                repo_data = data.pop('repo')
                actor = Actor.objects.filter((Q(id=actor_data.get('id')) \
                                    | Q(login=actor_data.get('login')))).first()
                if not actor:
                    actor = Actor.objects.create(**actor_data)
                repo, _ = Repo.objects.get_or_create(
                    id=repo_data.get('id'),
                    defaults={
                        'id': repo_data.get('id'),
                        'name': repo_data.get('name'),
                        'url': repo_data.get('url')
                    },
                )
                event = Event.objects.create(id=data.get('id'),
                                             repo=repo,
                                             actor=actor,
                                             created_at=data.get('created_at'),
                                             type=data.get('type'))
                return event
