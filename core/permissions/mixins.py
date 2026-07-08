from django.core.exceptions import PermissionDenied
from django.db.models import Q


class RowLevelPermissionMixin:
    """
    روی ListView/DetailView استفاده کن.
    باید feature_codename رو ست کنی.
    اگه مدل فیلد owner یا created_by نداره، owner_field رو عوض کن.
    """
    feature_codename = None
    owner_field = 'owner'

    def get_permission(self):
        profile = getattr(self.request.user, 'profile', None)
        if not profile or not profile.role:
            raise PermissionDenied

        try:
            return profile.role.permissions.get(feature__codename=self.feature_codename)
        except Exception:
            raise PermissionDenied

    def get_queryset(self):
        qs = super().get_queryset()
        permission = self.get_permission()

        if not permission.can_view:
            raise PermissionDenied

        if permission.scope == 'all':
            return qs

        if permission.scope == 'team':
            profile = self.request.user.profile
            team_user_ids = list(
                profile.team_members.values_list('user_id', flat=True)
            )
            team_user_ids.append(self.request.user.id)
            return qs.filter(**{f"{self.owner_field}__id__in": team_user_ids})

        # scope == 'own'
        return qs.filter(**{f"{self.owner_field}": self.request.user})
