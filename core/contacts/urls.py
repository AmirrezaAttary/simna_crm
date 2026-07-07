from django.urls import path

from . import views

urlpatterns = [
    path("", views.ContactListView.as_view(), name="contact-list"),
    path("<int:pk>/", views.ContactDetailView.as_view(), name="contact-detail"),
    path("leads/", views.LeadListView.as_view(), name="lead-list"),
]