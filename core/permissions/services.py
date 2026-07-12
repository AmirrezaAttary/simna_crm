from .models import Feature, RoleFeaturePermission, UserFeaturePermission


def get_effective_permission(user, feature_codename):
    """
    اولویت با UserFeaturePermission (override اختصاصی کاربر)؛
    اگر نبود سراغ RoleFeaturePermission بر اساس نقش پروفایل می‌رویم.
    خروجی: آبجکتی با can_view/can_add/can_edit/can_delete/scope یا None.
    """
    if not user or not user.is_authenticated:
        return None

    profile = getattr(user, "profile", None)
    if not profile:
        return None

    try:
        feature = Feature.objects.get(codename=feature_codename)
    except Feature.DoesNotExist:
        return None

    user_perm = UserFeaturePermission.objects.filter(profile=profile, feature=feature).first()
    if user_perm:
        return user_perm

    if profile.role_id:
        role_perm = RoleFeaturePermission.objects.filter(role=profile.role, feature=feature).first()
        if role_perm:
            return role_perm

    return None


def get_visible_feature_codenames(user):
    """مجموعه‌ی codename فیچرهایی که کاربر اجازه‌ی can_view روی آن‌ها را دارد."""
    if not user or not user.is_authenticated:
        return set()

    if user.is_superuser:
        return set(Feature.objects.values_list("codename", flat=True))

    profile = getattr(user, "profile", None)
    if not profile:
        return set()

    visible = set()

    if profile.role_id:
        role_view_codenames = RoleFeaturePermission.objects.filter(
            role=profile.role, can_view=True
        ).values_list("feature__codename", flat=True)
        visible.update(role_view_codenames)

    # override های اختصاصی کاربر: هم می‌توانند اضافه کنند هم می‌توانند دسترسی نقش را سلب کنند
    for perm in UserFeaturePermission.objects.filter(profile=profile).select_related("feature"):
        if perm.can_view:
            visible.add(perm.feature.codename)
        else:
            visible.discard(perm.feature.codename)

    return visible