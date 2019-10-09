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


raw_query = '''
    select actor_id, max(created_at) as date, count(*) as streak, login, avatar_url
    from (select actor_id, t1.created_at, login, avatar_url
      ,date(t1.created_at,-(select count(*) 
      from  RestAPI_event t2 
      where t2.actor_id = t1.actor_id 
      and t2.created_at<=t1.created_at)||' day') as grp
      from  RestAPI_event t1 inner join RestAPI_actor on t1.actor_id = RestAPI_actor.id) t
      group by actor_id
    '''

@api_view(['GET'])
def get_actors_by_longest_streak(request):
    raw_query_1 = '''
    SELECT actor_id as id,
            login,
           avatar_url,
    MIN(created_at) as start_date, 
    MAX(created_at) as end_date, 
    COUNT(*) as streak 
  from (select actor_id,
           created_at,
           login,
           avatar_url,
           (select count(*)
           from RestAPI_event EventsR
          where EventsR.actor_id = Events.actor_id 
           and  EventsR.created_at <= Events.created_at
            ) as event_group
            from RestAPI_event Events
            inner join RestAPI_actor on Events.actor_id = RestAPI_actor.id) A
            GROUP BY actor_id
            ORDER BY streak desc,
                     end_date desc,
                     login desc
                '''
    
    actors = dictfetchall(raw_query_1)
    return Response(actors)
