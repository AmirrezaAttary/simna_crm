from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from permissions.mixins import RowLevelPermissionMixin

from .models import Contact, Lead


class ContactListView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Contact
    template_name = "contacts/contact_list.html"
    context_object_name = "contacts"
    paginate_by = 25
    feature_codename = "contacts"
    owner_field = "owner"


class ContactDetailView(LoginRequiredMixin, RowLevelPermissionMixin, DetailView):
    model = Contact
    template_name = "contacts/contact_detail.html"
    context_object_name = "contact"
    feature_codename = "contacts"
    owner_field = "owner"


class LeadListView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Lead
    template_name = "contacts/lead_list.html"
    context_object_name = "leads"
    paginate_by = 25
    feature_codename = "leads"
    owner_field = "owner"
