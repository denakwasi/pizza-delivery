from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='sign_up'),
    path('all-users/', views.AllUsers.as_view(), name='all_users'),
    path('update-user/<str:user_id>/', views.UpdateUser.as_view(), name='update_user'),
    path('delete-user/<str:user_id>/', views.DeleteUser.as_view(), name='delete_user'),
    path('update-user-profile/<str:img_id>/', views.UpdateUserProfile.as_view(), name='update_user_profile'),
]