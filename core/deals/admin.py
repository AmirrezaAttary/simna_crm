from django.contrib import admin

from .models import Deal, Pipeline, Stage


class StageInline(admin.TabularInline):
    model = Stage
    extra = 1


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ("name", "is_default")
    inlines = [StageInline]


@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ("title", "pipeline", "stage", "amount", "owner", "expected_close_date")
    list_filter = ("pipeline", "stage")
    search_fields = ("title", "contact__first_name", "contact__last_name", "company__name")
    autocomplete_fields = ["contact", "company"]