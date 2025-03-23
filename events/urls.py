from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    #Home page
    path('', views.home, name='home'),
    #Create event
    path('create/', views.create_event_view, name='create_event'),
    #Event detail
    path('<int:event_id>/', views.event_detail_view, name='event_detail'),
    #Edit event
    path('<int:event_id>/edit/', views.edit_event, name='edit_event'),
    #Delete event
    path('<int:event_id>/delete/', views.delete_event, name='delete_event'),
    #Join event
    path('<int:event_id>/join/', views.join_event, name='join_event'),
    #Quit event
    path('<int:event_id>/quit/', views.quit_event, name='quit_event'),

]