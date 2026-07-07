from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "پروفایل"


class UserAdmin(admin.ModelAdmin):
    inlines = [ProfileInline]
    list_display = ("username", "first_name", "last_name", "email", "is_staff")


# ثبت مجدد User به همراه Profile inline
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    list_filter = ("role",)
    search_fields = ("user__username", "user__first_name", "user__last_name", "phone")