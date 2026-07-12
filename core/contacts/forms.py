from django import forms

from .models import Contact, Lead

INPUT = "w-full border border-gray-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-400 transition"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["first_name", "last_name", "email", "phone", "job_title", "company"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً علی"}),
            "last_name": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً رضایی"}),
            "email": forms.EmailInput(attrs={"class": INPUT}),
            "phone": forms.TextInput(attrs={"class": INPUT}),
            "job_title": forms.TextInput(attrs={"class": INPUT}),
            "company": forms.Select(attrs={"class": INPUT}),
        }


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["first_name", "last_name", "email", "phone", "company_name", "status", "source"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً علی"}),
            "last_name": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً رضایی"}),
            "email": forms.EmailInput(attrs={"class": INPUT}),
            "phone": forms.TextInput(attrs={"class": INPUT}),
            "company_name": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً شرکت آریا صنعت"}),
            "status": forms.Select(attrs={"class": INPUT}),
            "source": forms.Select(attrs={"class": INPUT}),
        }