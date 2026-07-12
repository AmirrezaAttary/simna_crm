from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "activities/task_list.html"
    context_object_name = "tasks"
    paginate_by = 25

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user).order_by("is_done", "due_date")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "activities/task_form.html"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)