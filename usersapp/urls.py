from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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

    path('api/users/', views.UserList.as_view(), name='user-list'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('api/users/me/', views.UserProfileView.as_view(), name='user-profile'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

"""
API cheat sheet:

GET /api/users/: Requires admin privileges.
GET /api/users/{id}/: Requires admin privileges.
GET /api/users/me/: Requires authentication.
PUT /api/users/me/: Requires authentication.
POST /api/auth/token/: Obtain a JWT token.
POST /api/auth/token/refresh/: Refresh the JWT token.
"""