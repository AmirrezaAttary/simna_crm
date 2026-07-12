from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.views.generic import CreateView, DeleteView, UpdateView

from .models import RoleFeaturePermission
from .services import get_effective_permission


class FeaturePermissionMixin:
    """
    قبل از اجرای هر ویو بررسی می‌کند که کاربر برای feature_codename
    اجازه‌ی متناسب با نوع ویو (view/add/edit/delete) را دارد یا نه.
    """
    feature_codename = None

    def get_feature_codename(self):
        if not self.feature_codename:
            raise ImproperlyConfigured(
                f"{self.__class__.__name__} باید feature_codename را مشخص کند."
            )
        return self.feature_codename

    def get_required_action(self):
        if isinstance(self, CreateView):
            return "add"
        if isinstance(self, UpdateView):
            return "edit"
        if isinstance(self, DeleteView):
            return "delete"
        return "view"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("برای دسترسی باید وارد حساب کاربری خود شوید.")

        if request.user.is_superuser:
            self.current_permission = None
            return super().dispatch(request, *args, **kwargs)

        permission = get_effective_permission(request.user, self.get_feature_codename())
        action = self.get_required_action()

        if not permission or not getattr(permission, f"can_{action}", False):
            raise PermissionDenied("شما اجازه دسترسی به این بخش را ندارید.")

        self.current_permission = permission
        return super().dispatch(request, *args, **kwargs)

    def get_action_flags(self):
        """
        فلگ‌های can_view/add/edit/delete برای استفاده در تمپلیت
        (مثلاً نمایش/مخفی کردن دکمه‌های ویرایش و حذف در لیست).
        """
        # if self.request.user.is_superuser:
        #     return {"can_view": True, "can_add": True, "can_edit": True, "can_delete": True}

        permission = getattr(self, "current_permission", None)
        if not permission:
            return {"can_view": False, "can_add": False, "can_edit": False, "can_delete": False}

        return {
            "can_view": permission.can_view,
            "can_add": permission.can_add,
            "can_edit": permission.can_edit,
            "can_delete": permission.can_delete,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["feature_perms"] = self.get_action_flags()
        return context


class RowLevelPermissionMixin(FeaturePermissionMixin):
    """
    علاوه بر بررسی دسترسی فیچر، بر اساس scope (own/team/all) کوئری‌ست
    و تک‌رکورد را محدود می‌کند تا کاربر فقط رکوردهای مجاز خودش را ببیند.
    """
    owner_field = "owner"

    def get_current_scope(self):
        if getattr(self, "current_permission", None) is None:
            return RoleFeaturePermission.ALL
        return self.current_permission.scope

    def get_team_user_ids(self):
        return [self.request.user.id]

    def get_queryset(self):
        queryset = super().get_queryset()
        scope = self.get_current_scope()

        if scope == RoleFeaturePermission.ALL:
            return queryset
        if scope == RoleFeaturePermission.TEAM:
            return queryset.filter(**{f"{self.owner_field}__in": self.get_team_user_ids()})
        return queryset.filter(**{self.owner_field: self.request.user})

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        scope = self.get_current_scope()

        if scope == RoleFeaturePermission.ALL:
            return obj

        owner = getattr(obj, self.owner_field, None)
        owner_id = getattr(owner, "id", None)
        allowed_ids = self.get_team_user_ids() if scope == RoleFeaturePermission.TEAM else [self.request.user.id]

        if owner_id not in allowed_ids:
            raise PermissionDenied("شما اجازه دسترسی به این رکورد را ندارید.")

        return obj