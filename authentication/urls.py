from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='sign_up'),
    path('all-users/', views.AllUsers.as_view(), name='all_users'),
]