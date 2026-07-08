from django.contrib import admin
from .models import Feature, Role, RoleFeaturePermission


class RoleFeaturePermissionInline(admin.TabularInline):
    model = RoleFeaturePermission
    extra = 1


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'parent', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'codename')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename')
    search_fields = ('name', 'codename')
    inlines = [RoleFeaturePermissionInline]
