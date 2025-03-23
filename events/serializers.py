from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Event, EventParticipant

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing events
    """
    organizer = UserSerializer(source='owner', read_only=True)
    participants_count = serializers.IntegerField(source='current_participants', read_only=True)
    event_type = serializers.CharField(source='type')

    class Meta:
        model = Event
        fields = [
            'id', 
            'title', 
            'description', 
            'date',
            'location', 
            'organizer',
            'participants_count',
            'max_participants',
            'event_type'
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed event view
    """
    organizer = UserSerializer(source='owner', read_only=True)
    participants_count = serializers.IntegerField(source='current_participants', read_only=True)
    event_type = serializers.CharField(source='type')
    participants = serializers.SerializerMethodField()
    average_rating = serializers.FloatField(source='average_rating', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 
            'title', 
            'description', 
            'date',
            'location', 
            'organizer',
            'participants_count',
            'max_participants',
            'event_type',
            'participants',
            'average_rating',
            'start_time',
            'end_time'
        ]

    def get_participants(self, obj):
        """
        Get list of participants for the event
        """
        participants = EventParticipant.objects.filter(event=obj)
        return UserSerializer(
            [participant.participant for participant in participants], 
            many=True
        ).data 