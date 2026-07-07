from django.contrib import admin

from .models import Call, Meeting, Note, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "due_date", "is_done", "assigned_to")
    list_filter = ("priority", "is_done")
    search_fields = ("title", "description")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("content", "created_by", "created_at")
    search_fields = ("content",)


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ("direction", "duration_minutes", "performed_by", "created_at")
    list_filter = ("direction",)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "scheduled_at", "location", "organizer")
    search_fields = ("title", "location")