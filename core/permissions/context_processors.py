from .models import Feature


def sidebar_menu(request):

    if not request.user.is_authenticated:
        return {
            "sidebar_features": []
        }

    profile = getattr(request.user, "profile", None)

    if not profile or not profile.role:
        return {
            "sidebar_features": []
        }


    features = Feature.objects.filter(
        role_permissions__role=profile.role,
        role_permissions__can_view=True,
        parent=None
    ).prefetch_related(
        "children"
    ).distinct()


    return {
        "sidebar_features": features
    }