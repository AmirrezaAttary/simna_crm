from django.db import models


class Feature(models.Model):
    codename = models.CharField(
        max_length=100,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    icon = models.CharField(
        max_length=50,
        blank=True
    )

    url_name = models.CharField(
        max_length=100,
        blank=True
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name


class Role(models.Model):
    codename = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class RoleFeaturePermission(models.Model):

    OWN = "own"
    TEAM = "team"
    ALL = "all"

    SCOPE_CHOICES = [
        (OWN, "فقط خودش"),
        (TEAM, "تیم"),
        (ALL, "همه"),
    ]

    role = models.ForeignKey(
        Role,
        related_name="permissions",
        on_delete=models.CASCADE
    )

    feature = models.ForeignKey(
        Feature,
        related_name="role_permissions",
        on_delete=models.CASCADE
    )

    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    scope = models.CharField(
        max_length=10,
        choices=SCOPE_CHOICES,
        default=OWN
    )

    class Meta:
        unique_together = ("role", "feature")

    def __str__(self):
        return f"{self.role} | {self.feature}"


class UserFeaturePermission(models.Model):

    profile = models.ForeignKey(
        "accounts.Profile",
        related_name="user_permissions",
        on_delete=models.CASCADE
    )

    feature = models.ForeignKey(
        Feature,
        related_name="user_permissions",
        on_delete=models.CASCADE
    )

    can_view = models.BooleanField(default=False)
    can_add = models.BooleanField(default=False)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    scope = models.CharField(
        max_length=10,
        choices=RoleFeaturePermission.SCOPE_CHOICES,
        default=RoleFeaturePermission.OWN
    )

    class Meta:
        unique_together = ("profile", "feature")

    def __str__(self):
        return f"{self.profile.user.username} | {self.feature}"