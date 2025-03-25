from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator

from rest_framework import generics, permissions

from django.contrib.auth.models import User
from .models import Event, EventParticipant, EventComment, StarReview
from .forms import EventForm, EventCommentForm, ReviewForm
from datetime import datetime, date, time


# Create your views here.
def home(request):
    """
    Home page for the events app
    """
    events = Event.objects.all()
    paginator = Paginator(events, 21)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events/home.html', {'page_obj': page_obj})


"""
EVENT VIEWS
"""
@login_required
def create_event_view(request):
    """
    Create a new event
    """
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            return redirect('events:event_detail', event.id)
        else:
            print(form.errors)
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def event_detail_view(request, event_id):
    """
    Display details of a specific event
    """
    event = get_object_or_404(Event, id=event_id)
    average_rating = event.average_rating()
    return render(request, 'events/event_detail.html', {'event': event, 'average_rating': average_rating})

@login_required
def join_event(request, event_id):
    """
    Join event with checks
    - Check if user is already registered
    - Check if event is full
    - Check if event has already ended
    """
    event = get_object_or_404(Event, id=event_id)

    current_datetime = datetime.now()
    event_datetime = datetime.combine(event.date, event.end_time)
    
    if event_datetime < current_datetime:
        messages.error(request, "This event has already ended!")
        return redirect('events:event_detail', event_id)

    if event.is_participant(request.user):
        messages.error(request, "You are already registered for this event!")
        return redirect('events:event_detail', event_id)
    
    if event.current_participants >= event.max_participants:
        messages.error(request, "This event is full!")
        return redirect('events:event_detail', event_id)
    
    EventParticipant.objects.create(event=event, participant=request.user)
    event.current_participants += 1
    event.save()
    messages.success(request, "You have successfully joined the event!")
    return redirect('events:event_detail', event_id)

@login_required
def quit_event(request, event_id):
    """
    Quit an event
    """
    event = get_object_or_404(Event, id=event_id)
    
    if not event.is_participant(request.user):
        messages.error(request, "You are not registered for this event!")
        return redirect('events:event_detail', event_id)
    
    event.remove_participant(request.user)
    messages.success(request, "You have successfully quit the event!")
    return redirect('events:event_detail', event_id)

@login_required
def edit_event(request, event_id):
    """
    Edit an event
    """
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_detail', event_id)
        else:
            print(form.errors)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form})

@login_required
def delete_event(request, event_id):
    """
    Delete an event
    """
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('events:home')

@login_required
def add_comment(request, event_id):
    """
    Add a comment to an event
    """
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.event = event
            comment.user = request.user
            comment.save()
            return redirect('events:event_detail', event_id)
        else:
            print(form.errors)
    else:
        form = EventCommentForm()
    return render(request, 'events/add_comment.html', {'form': form})

@login_required
def add_review(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if StarReview.objects.filter(event=event, user=request.user).exists():
        messages.error(request, "You have already reviewed this event.")
        return redirect('events:event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect('events:event_detail', event_id=event_id)
    else:
        form = ReviewForm()
    
    return render(request, 'events/add_review.html', {'form': form, 'event': event})


