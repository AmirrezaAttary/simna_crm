from django.urls import path

from .views import (
    DealCreateView,
    DealDetailView,
    DealListView,
    PipelineBoardView,
)

urlpatterns = [
    path("deals/", DealListView.as_view(), name="deal-list"),
    path("deals/new/", DealCreateView.as_view(), name="deal-create"),
    path("deals/<int:pk>/", DealDetailView.as_view(), name="deal-detail"),
    path("pipeline/", PipelineBoardView.as_view(), name="pipeline-board"),
]