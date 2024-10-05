from django.db.models import Q
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer

from rest_framework.views import APIView
# Create your views here.

class EventCreate(generics.ListCreateAPIView):
    """
    `POST` - Creates a new events
    `GET` - Lists out all existing events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    lookup_field = 'pk'

class EventFind(APIView):
    def get(self, request, format=None):
        """

        Available query parameters:

        1. `/event_find/` -- Displays all available events
         2. `/event_find/?title=<title>&content=<content>` -- Finds all events with that title and/or content  
        """ 
        title = request.query_params.get("title", "")
        content = request.query_params.get("content", "")

        # Use Q objects to filter by title and content simultaneously
        if title or content:
            event = Event.objects.filter(
                Q(title__icontains=title) | Q(content__icontains=content)
            )
        else:
            event = Event.objects.all()

        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)