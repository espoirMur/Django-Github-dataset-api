# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from .models import Event, Actor
from .serializers import EventSerializer, ActorSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import connection

'''
The endpoints we are looking for :
    - Done Erasing all the events
    - Done Adding new events
    - Done Returning all the events
    - Done Returning the event records filtered by the actor ID
    - Updating the avatar URL of the actor
    - turning the actor records ordered by the total number of event
    - Returning the actor records ordered by the maximum streak


'''


@api_view(["DELETE"])
def delete_all_events(request):
    Event.objects.all().delete()
    return Response(status=status.HTTP_200_OK)


class GetPostEventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer



@api_view(['GET'])
def get_events_by_actor_id(request, actor_id):
    actor_id = int(actor_id)
    get_object_or_404(Actor, pk=actor_id)
    events = Event.objects.filter(actor_id=actor_id).order_by('id').all()
    if request.method == 'GET':
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)




@api_view(['GET'])
def get_actors(request):
    raw_query = '''
    select RestAPI_actor.id,
           RestAPI_actor.login,
           RestAPI_actor.avatar_url,
           count(RestAPI_event.id) as events_organized
           from RestAPI_actor
           inner join RestAPI_event
           on RestAPI_event.actor_id = RestAPI_actor.id
           group by RestAPI_event.actor_id
           order by events_organized desc,
                    RestAPI_event.created_at desc,
                    RestAPI_actor.login desc
                '''
    actors = Actor.objects.raw(raw_query)
    serializer = ActorSerializer(actors, many=True)
    return Response(serializer.data)
