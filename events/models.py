from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    start_time = models.TimeField(default='12:00:00')
    end_time = models.TimeField(default='13:00:00')
    location = models.CharField(max_length=200)
    max_participants = models.IntegerField()
    current_participants = models.IntegerField(default=0)
    type = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    star_review = models.FloatField(default=0)

    def is_participant(self, user):
        """
        Check if a user is a participant of an event
        """
        return EventParticipant.objects.filter(event=self, participant=user).exists()

    def remove_participant(self, user):
        """
        Remove a participant from an event
        """
        EventParticipant.objects.filter(event=self, participant=user).delete()
        self.current_participants -= 1
        self.save()

    def average_rating(self):
        """
        Calculate the average rating of an event
        """
        reviews = self.starreview_set.all()
        if reviews.exists():
            return sum(review.star_review for review in reviews) / reviews.count()
        return None
        
    def __str__(self):
        return self.title

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.participant.username} joined {self.event.title}"


class EventComment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment} - {self.event.title}"
    
class StarReview(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    star_review = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')

    def __str__(self):
        return f"{self.star_review} - {self.event.title}"
    