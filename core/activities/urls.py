from django.urls import path

from .views import TaskCreateView, TaskListView

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),
]