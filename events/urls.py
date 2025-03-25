from django.urls import path
from . import views
from .api import apiviews
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
    #Add comment
    path('<int:event_id>/add_comment/', views.add_comment, name='add_comment'),
    #Add star review
    path('<int:event_id>/add_review/', views.add_review, name='add_review'),

    #API
    path('api/events/', apiviews.EventList.as_view(), name='event-list'),
    path('api/events/<int:pk>/', apiviews.EventDetail.as_view(), name='event-detail'),
    path('api/events/<int:event_id>/comments/', apiviews.CommentList.as_view(), name='event-comment-list'),
    path('api/events/<int:event_id>/rate/', apiviews.EventReviewsStats.as_view(), name='event-review-rate'),
    path('api/events/<int:event_id>/ratings/', apiviews.EventReviewList.as_view(), name='event-ratings'),
]

"""
POST /api/events/{id}/rate/ - ocena wydarzenia
GET /api/events/{id}/ratings/ - statystyki ocen wydarzenia
"""