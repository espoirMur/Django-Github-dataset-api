# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from rest_framework.views import APIView
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


class ActorView(APIView):
    serializer = ActorSerializer

    def get(self, request):
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

    def put(self, request):
        actor_data = request.data
        serializer = ActorSerializer(data=actor_data)
        serializer.is_valid(raise_exception=True)
        actor_data = serializer.data
        actor = get_object_or_404(Actor, pk=actor_data.get('id'))
        if actor.login != actor_data.get('login'):
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': "should not update the login"})
        actor.avatar_url = actor_data.get("avatar_url")
        actor.save()
        return Response(serializer.data)



def dictfetchall(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()
        ]


@api_view(['GET'])
def get_actors_by_longest_streak(request):
    raw_query = '''
    select RestAPI_actor.id,
           RestAPI_actor.login,
           RestAPI_actor.avatar_url,
           count(*) as streak,
           min RestAPI_event.created_at as from_date,
           max RestAPI_event.created_at  as to_date
           from (select RestAPI_event.created_at,
                 RestAPI_event.actor_id,
                 row_number() over 
                 (partition by RestAPI_event.actor_id order by RestAPI_event.created_at)
                  as seqnum
                  from RestAPI_actor
                  inner join RestAPI_event
                  on RestAPI_event.actor_id = RestAPI_actor.id
           ) RestAPI_event.actor
           group by RestAPI_event.actor_id, ( RestAPI_event.created_at - seqnum)
                '''
    actors = dictfetchall(raw_query)
    return Response(actors)
