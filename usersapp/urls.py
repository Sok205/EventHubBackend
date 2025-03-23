from django.urls import path
from . import views

app_name = 'usersapp'

urlpatterns = [
    # LOGIN AND REGISTER VIEWS
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # PROFILE VIEWS
    path('profiles/', views.all_profile_view, name='profiles'),
    path('profiles/<str:username>/', views.profile_view, name='profile'),
    # PROFILE FORM EDITION
    path('profiles/<str:username>/edit/', views.profile_form_edition_view, name='profile_form_edition'),
]