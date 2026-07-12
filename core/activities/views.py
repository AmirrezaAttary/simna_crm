from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from permissions.mixins import RowLevelPermissionMixin

from .forms import TaskForm
from .models import Task


class TaskListView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Task
    template_name = "activities/task_list.html"
    context_object_name = "tasks"
    paginate_by = 25
    feature_codename = "tasks"
    owner_field = "assigned_to"

    def get_queryset(self):
        return super().get_queryset().order_by("is_done", "due_date")


class TaskCreateView(LoginRequiredMixin, RowLevelPermissionMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "activities/task_form.html"
    feature_codename = "tasks"
    owner_field = "assigned_to"
    success_url = reverse_lazy("task-list")

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, RowLevelPermissionMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "activities/task_form.html"
    feature_codename = "tasks"
    owner_field = "assigned_to"
    success_url = reverse_lazy("task-list")


class TaskDeleteView(LoginRequiredMixin, RowLevelPermissionMixin, DeleteView):
    model = Task
    template_name = "activities/task_confirm_delete.html"
    context_object_name = "task"
    feature_codename = "tasks"
    owner_field = "assigned_to"
    success_url = reverse_lazy("task-list")