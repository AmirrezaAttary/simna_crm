from django.urls import path

from .views import (
    ContactCreateView,
    ContactDetailView,
    ContactListView,
    LeadCreateView,
    LeadListView,
)

urlpatterns = [
    path("contacts/", ContactListView.as_view(), name="contact-list"),
    path("contacts/new/", ContactCreateView.as_view(), name="contact-create"),
    path("contacts/<int:pk>/", ContactDetailView.as_view(), name="contact-detail"),
    path("leads/", LeadListView.as_view(), name="lead-list"),
    path("leads/new/", LeadCreateView.as_view(), name="lead-create"),
]