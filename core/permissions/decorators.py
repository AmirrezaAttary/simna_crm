from functools import wraps
from django.core.exceptions import PermissionDenied


def require_feature(codename, action='can_view'):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            profile = getattr(request.user, 'profile', None)
            if not profile or not profile.role:
                raise PermissionDenied

            permission = profile.role.permissions.filter(
                feature__codename=codename
            ).first()

            if not permission or not getattr(permission, action, False):
                raise PermissionDenied

            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
