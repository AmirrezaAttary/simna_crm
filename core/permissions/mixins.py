from django.core.exceptions import PermissionDenied


class RowLevelPermissionMixin:

    feature_codename = None

    owner_field = "owner"


    def get_permission(self):

        profile = getattr(
            self.request.user,
            "profile",
            None
        )

        if not profile or not profile.role:
            raise PermissionDenied


        permission = profile.role.permissions.filter(
            feature__codename=self.feature_codename
        ).first()


        if not permission:
            raise PermissionDenied


        return permission



    def get_queryset(self):

        qs = super().get_queryset()

        permission = self.get_permission()


        if not permission.can_view:
            raise PermissionDenied



        if permission.scope == "all":
            return qs



        if permission.scope == "own":

            return qs.filter(
                **{
                    self.owner_field:
                    self.request.user
                }
            )


        return qs