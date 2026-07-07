from django.urls import path

from . import views

urlpatterns = [
    path("", views.DealListView.as_view(), name="deal-list"),
    path("deals/<int:pk>/", views.DealDetailView.as_view(), name="deal-detail"),
    path("pipeline/", views.pipeline_board, name="pipeline-board"),
]