from django.urls import path
from .views import allTasks
# from .views import NewTask, allTasks

urlpatterns = [
    path('', allTasks),
    # path('new-task/', NewTask.as_view())
]