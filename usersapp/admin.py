from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile
from events.models import Event, EventParticipant, EventComment, StarReview
# Register your models here.
admin.site.unregister(User)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'email')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location', )
    search_fields = ('user__username', 'bio', 'location')
    list_filter = ('location',)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'date', 'start_time', 'end_time', 'location', 'max_participants', 'current_participants', 'type')
    search_fields = ('title', 'owner__username', 'location', 'type')
    list_filter = ('location', 'type')


class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'participant', 'joined_at')
    search_fields = ('event__title', 'participant__username')
    list_filter = ('event__location', 'event__type')

class EventCommentAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'comment', 'created_at')
    search_fields = ('event__title', 'user__username', 'comment')
    list_filter = ('event__location', 'event__type')

class StarReviewAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'star_review', 'created_at')
    search_fields = ('event__title', 'user__username')
    list_filter = ('event__location', 'event__type')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventParticipant, EventParticipantAdmin)
admin.site.register(EventComment, EventCommentAdmin)
admin.site.register(StarReview, StarReviewAdmin)