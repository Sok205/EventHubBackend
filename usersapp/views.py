from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile
from events.models import EventParticipant, Event
from .forms import ProfileFormEdition
from .api.seriallizers import ProfileSerializer, UserSerializer, UserUpdateSerializer, ProfileUpdateSerializer

"""
LOGIN AND REGISTER VIEWS
"""

def register_view(request):
    """
    Register a new user
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('events:home')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UserCreationForm()
    return render(request, 'usersapp/register.html', {'form': form})

@login_required
def logout_view(request):
    """
    Logout a user
    """
    logout(request)
    return redirect('usersapp:login')

def login_view(request):
    """
    Login a user
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('events:home')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = AuthenticationForm()
    return render(request, 'usersapp/login.html', {'form': form})

"""
PROFILE VIEWS
"""
@login_required
def all_profile_view(request):
    """
    View a user's profile
    """
    profiles = Profile.objects.all()
    return render(request, 'usersapp/profiles.html', {'profiles': profiles})

@login_required
def profile_view(request, username):
    """
    View a user's profile
    """
    profile = Profile.objects.get(user__username=username)
    participating_events = EventParticipant.objects.filter(participant=profile.user)
    return render(request, 'usersapp/profile.html', {'profile': profile, 'participating_events': participating_events})


@login_required
def profile_form_edition_view(request, username):
    """
    Edit a user's profile
    """
    profile = Profile.objects.get(user__username=username)
    
    if request.method == 'POST':
        form = ProfileFormEdition(request.POST, request.FILES, instance=profile)
        
        if 'profile_picture' in request.FILES:
            print(f"File uploaded: {request.FILES['profile_picture'].name}")
        else:
            print("No file uploaded in request.FILES")
            
        if form.is_valid():
            profile = form.save()
            print(f"Profile saved. Image path: {profile.profile_picture.path if profile.profile_picture else 'No image'}")
            messages.success(request, 'Profile updated successfully')
            return redirect('usersapp:profile', username=username)
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, 'Please correct the errors below')
    else:
        form = ProfileFormEdition(instance=profile)
    return render(request, 'usersapp/profile_form_edition.html', {'form': form})


    