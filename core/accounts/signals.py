from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_profile(sender, instance, created, **kwargs):
    """با ساخته شدن هر User، یک Profile متناظر به‌صورت خودکار ساخته می‌شود."""
    if created:
        Profile.objects.create(user=instance)
    else:
        # اگر پروفایل به هر دلیلی وجود نداشت، بسازش
        Profile.objects.get_or_create(user=instance)