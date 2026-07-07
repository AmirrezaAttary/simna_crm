from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class RelatedObjectMixin(models.Model):
    """
    Mixin برای اتصال هر فعالیت به هر مدل دیگری (Deal، Contact، Lead و ...)
    با استفاده از GenericForeignKey.
    """

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, blank=True
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        abstract = True


class TaskPriority(models.TextChoices):
    LOW = "low", "کم"
    MEDIUM = "medium", "متوسط"
    HIGH = "high", "بالا"


class Task(RelatedObjectMixin):
    """کار/یادآوری برای پیگیری یک Lead، Contact یا Deal"""

    title = models.CharField(max_length=200, verbose_name="عنوان")
    description = models.TextField(blank=True)
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="سررسید")
    priority = models.CharField(max_length=10, choices=TaskPriority.choices, default=TaskPriority.MEDIUM)
    is_done = models.BooleanField(default=False, verbose_name="انجام شده")
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تسک"
        verbose_name_plural = "تسک‌ها"
        ordering = ["due_date"]

    def __str__(self):
        return self.title


class Note(RelatedObjectMixin):
    """یادداشت آزاد روی یک Lead، Contact یا Deal"""

    content = models.TextField(verbose_name="متن یادداشت")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="notes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "یادداشت"
        verbose_name_plural = "یادداشت‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return self.content[:50]


class CallDirection(models.TextChoices):
    INBOUND = "inbound", "ورودی"
    OUTBOUND = "outbound", "خروجی"


class Call(RelatedObjectMixin):
    """ثبت تماس تلفنی"""

    direction = models.CharField(max_length=10, choices=CallDirection.choices, default=CallDirection.OUTBOUND)
    duration_minutes = models.PositiveIntegerField(default=0)
    summary = models.TextField(blank=True, verbose_name="خلاصه تماس")
    performed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="calls"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تماس"
        verbose_name_plural = "تماس‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"تماس {self.get_direction_display()} - {self.created_at:%Y-%m-%d}"


class Meeting(RelatedObjectMixin):
    """جلسه (حضوری یا آنلاین)"""

    title = models.CharField(max_length=200, verbose_name="عنوان جلسه")
    scheduled_at = models.DateTimeField(verbose_name="زمان برگزاری")
    location = models.CharField(max_length=200, blank=True, verbose_name="محل / لینک برگزاری")
    notes = models.TextField(blank=True)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="meetings"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "جلسه"
        verbose_name_plural = "جلسات"
        ordering = ["scheduled_at"]

    def __str__(self):
        return self.title