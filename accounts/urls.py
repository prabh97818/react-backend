from django.urls import path
from .views import current_user, UserList, approve_account, all_users

urlpatterns = [
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('approve-account/<token>', approve_account),
    path('all-user/', all_users)
]