from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


def register_view(request):
    """
    Register a new user
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('usersapp:login')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = UserCreationForm()
    return render(request, 'usersapp/register.html', {'form': form})

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

