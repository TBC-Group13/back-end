from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserReputationAPIView, UserSettingsView, \
    UserLogoutView, UserReputationListAPIView, DeleteUserView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/<int:user_id>/reputation/', UserReputationAPIView.as_view(), name='user-reputation'),
    path('user/settings/', UserSettingsView.as_view(), name='user-settings'),
    path('users/reputation/', UserReputationListAPIView.as_view(), name='user-reputation-list'),
    path('users/delete/', DeleteUserView.as_view(), name='user-delete'),
]

