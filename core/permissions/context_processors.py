from .models import Feature, RoleFeaturePermission


def sidebar_menu(request):
    if not request.user.is_authenticated:
        return {'sidebar_menu': []}

    profile = getattr(request.user, 'profile', None)
    if not profile or not profile.role:
        return {'sidebar_menu': []}

    allowed_ids = RoleFeaturePermission.objects.filter(
        role=profile.role, can_view=True
    ).values_list('feature_id', flat=True)

    menu = Feature.objects.filter(
        id__in=allowed_ids, parent=None
    ).prefetch_related('children').order_by('order')

    return {'sidebar_menu': menu}
