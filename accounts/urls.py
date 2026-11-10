from django.urls import path
from .views import LoginView, MeView, LogoutView, GoogleLoginView, GuestLoginView, UserSearchListView

urlpatterns = [
    path('google/', GoogleLoginView.as_view(), name='google-login'),
    path('login/', LoginView.as_view(), name='login'),
    path('guest-login/', GuestLoginView.as_view(), name='guest-login'),
    path('users/', UserSearchListView.as_view(), name='user-search-list'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
