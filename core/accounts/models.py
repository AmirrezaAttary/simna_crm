from django.conf import settings
from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin", "مدیر سیستم"
    SALES_MANAGER = "sales_manager", "مدیر فروش"
    SALES_REP = "sales_rep", "کارشناس فروش"
    SUPPORT = "support", "پشتیبانی"


class Profile(models.Model):
    """
    اطلاعات تکمیلی کاربر (بدون نیاز به override کردن مدل User).
    برای هر User به صورت خودکار یک Profile ساخته می‌شود (signals.py).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.SALES_REP)
    phone = models.CharField(max_length=20, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "پروفایل کاربر"
        verbose_name_plural = "پروفایل‌های کاربران"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"