from django.contrib import admin

from .models import Company, Contact, Lead


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "industry", "phone", "owner")
    search_fields = ("name", "industry")
    list_filter = ("industry",)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company_name", "status", "source", "owner", "created_at")
    list_filter = ("status", "source")
    search_fields = ("first_name", "last_name", "email", "phone", "company_name")


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name", "company", "email", "phone", "owner")
    list_filter = ("company",)
    search_fields = ("first_name", "last_name", "email", "phone")