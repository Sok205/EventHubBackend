from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from events.models import Event, EventComment, StarReview
from events.api.serializers import EventListSerializer, EventDetailSerializer, CommentSerializer, StarReviewSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

"""
API VIEWS
"""

class EventList(generics.ListCreateAPIView):
    """
    List all events or create a new event
    """
    queryset = Event.objects.all()
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an event
    """
    queryset = Event.objects.all()
    serializer_class = EventDetailSerializer
    permission_classes = [IsAuthenticated]

class CommentList(generics.ListCreateAPIView):
    """
    List all commments from a single event
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    #filtering events by id 
    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return EventComment.objects.filter(id=event_id)

    def perform_create(self, serializer):
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event, event_id=event_id)
        serializer.save(owner=self.request.user, event=event)


class EventReviewsStats(generics.RetrieveAPIView):
    serializer_class = StarReviewSerializer
    permission_classes = [IsAuthenticated]

    #Get the object
    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return get_object_or_404(Event, id=event_id)

    #Retrieve only avg rating
    def retrieve(self, request, *args, **kwargs):
        event = self.get_queryset()
        avg_rating = event.average_rating()
        return Response({"avg_rating": avg_rating})

    #Rate the event
    def perform_create(self, serializer):
        event_id = self.kwargs["event_id"]
        event = get_object_or_404(Event, event_id=event_id)
        serializer.save(owner=self.request.user, event=event)

class EventReviewList(generics.ListAPIView):
    serializer_class = StarReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs["event_id"]
        return StarReview.objects.filter(event = event_id)





