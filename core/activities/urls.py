from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskListView,
    TaskUpdateView,
)

urlpatterns = [
    path("tasks/", TaskListView.as_view(), name="task-list"),
    path("tasks/new/", TaskCreateView.as_view(), name="task-create"),
    path("tasks/<int:pk>/edit/", TaskUpdateView.as_view(), name="task-edit"),
    path("tasks/<int:pk>/delete/", TaskDeleteView.as_view(), name="task-delete"),
]