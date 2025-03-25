from rest_framework import serializers
from django.contrib.auth.models import User
from ..models import Event, EventParticipant, EventComment, StarReview
from usersapp.api.seriallizers import UserSerializer


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
    average_rating = serializers.FloatField(read_only=True)

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

    def get_average_rating(self, obj):
        return obj.average_rating()
    
class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for event comments 
    """
    user = UserSerializer(read_only=True)
    event = EventDetailSerializer(read_only=True)

    class Meta:
        model = EventComment
        fields = ['id','event','user','comment','created_at']
        read_only_field = ["id","event","user","created_at"]

class StarReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer

    class Meta:
        model = StarReview
        fields = "__all__"
        read_only_fields = ["id","event","user","created_at"]
"""
class StarReview(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star_review = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.star_review} - {self.event.title}"
"""