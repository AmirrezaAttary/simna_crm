from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "activities/task_list.html"
    context_object_name = "tasks"
    paginate_by = 25

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by("is_done", "due_date")