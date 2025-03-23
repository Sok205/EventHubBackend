from django.shortcuts import render

# Create your views here.
def home(request):
    """
    Home page for the events app
    """
    return render(request, 'events/home.html')