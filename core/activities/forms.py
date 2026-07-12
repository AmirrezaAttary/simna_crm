from django import forms

from .models import Task

INPUT = "w-full border border-gray-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-400 transition"


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "priority", "due_date"]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً پیگیری تماس با مشتری"}),
            "priority": forms.Select(attrs={"class": INPUT}),
            # due_date روی مدل DateTimeField هست، نه Date
            "due_date": forms.DateTimeInput(attrs={"class": INPUT, "type": "datetime-local"}, format="%Y-%m-%dT%H:%M"),
        }