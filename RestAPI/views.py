# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from .models import Event, Actor, Repo
from .serializers import EventSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.status import HTTP_200_OK

'''
The endpoints we are looking for :
    - Erasing all the events
    - Adding new events
    - Returning all the events
    - Returning the event records filtered by the actor ID
    - Updating the avatar URL of the actor
    - turning the actor records ordered by the total number of event
    - Returning the actor records ordered by the maximum streak


'''


@api_view(["DELETE"])
def delete_all_events(request):
    Event.objects.all().delete()
    return Response(status=HTTP_200_OK)


class GetPostEventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

"""
@api_view(['GET'])
def get_all_events(request):
    events = Event.objects.all()
    print(events, '======>')
    data = EventSerializer(events, many=True)
    return Response(status=status.HTTP_200_OK, data=data.data)"""
