from django import template

register = template.Library()

@register.filter
def is_participant(event, user):
    """
    Check if a user is a participant of an event
    """
    return event.is_participant(user)