# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from .models import Event,Actor
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import get_object_or_404

'''
The endpoints we are looking for :
    - Done Erasing all the events
    - Done Adding new events
    - Done Returning all the events
    - Returning the event records filtered by the actor ID
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


class GetEventByActor(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'actor_id'

    def get_object(self):
        queryset = self.get_queryset()
        actor_id = self.kwargs['actor_id']

        print(queryset, )
        data = queryset.filter(actor_id=actor_id)
        return data
