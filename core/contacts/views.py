from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from permissions.mixins import RowLevelPermissionMixin

from .forms import ContactForm, LeadForm
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


class ContactCreateView(LoginRequiredMixin, RowLevelPermissionMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contacts/contact_form.html"
    feature_codename = "contacts"
    owner_field = "owner"
    success_url = reverse_lazy("contact-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LeadListView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Lead
    template_name = "contacts/lead_list.html"
    context_object_name = "leads"
    paginate_by = 25
    feature_codename = "leads"
    owner_field = "owner"


class LeadCreateView(LoginRequiredMixin, RowLevelPermissionMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "contacts/lead_form.html"
    feature_codename = "leads"
    owner_field = "owner"
    success_url = reverse_lazy("lead-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)