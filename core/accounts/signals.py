from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from accounts.models import Profile
from permissions.models import Role

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_profile(sender, instance, created, **kwargs):

    if created:
        role = Role.objects.first()

        Profile.objects.create(
            user=instance,
            role=role
        )

    if hasattr(instance, "profile"):
        instance.profile.save()