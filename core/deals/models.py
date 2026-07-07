from django.conf import settings
from django.db import models

from contacts.models import Company, Contact


class Pipeline(models.Model):
    """یک خط فروش (مثلاً: فروش مستقیم، فروش سازمانی و ...)"""

    name = models.CharField(max_length=100, verbose_name="نام پایپ‌لاین")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "پایپ‌لاین"
        verbose_name_plural = "پایپ‌لاین‌ها"

    def __str__(self):
        return self.name


class Stage(models.Model):
    """مراحل داخل یک پایپ‌لاین (مثلاً: تماس اولیه، ارسال پیشنهاد، مذاکره، بسته‌شده)"""

    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name="stages")
    name = models.CharField(max_length=100, verbose_name="نام مرحله")
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")
    probability = models.PositiveIntegerField(
        default=0, help_text="درصد احتمال بسته شدن معامله در این مرحله (0 تا 100)"
    )
    is_won = models.BooleanField(default=False, verbose_name="مرحله برد")
    is_lost = models.BooleanField(default=False, verbose_name="مرحله باخت")

    class Meta:
        verbose_name = "مرحله"
        verbose_name_plural = "مراحل"
        ordering = ["pipeline", "order"]

    def __str__(self):
        return f"{self.pipeline.name} / {self.name}"


class Deal(models.Model):
    """فرصت فروش (Opportunity)"""

    title = models.CharField(max_length=200, verbose_name="عنوان معامله")
    contact = models.ForeignKey(
        Contact, on_delete=models.SET_NULL, null=True, blank=True, related_name="deals"
    )
    company = models.ForeignKey(
        Company, on_delete=models.SET_NULL, null=True, blank=True, related_name="deals"
    )
    pipeline = models.ForeignKey(Pipeline, on_delete=models.PROTECT, related_name="deals")
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT, related_name="deals")
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name="مبلغ")
    currency = models.CharField(max_length=10, default="IRR")
    expected_close_date = models.DateField(null=True, blank=True, verbose_name="تاریخ تخمینی بسته‌شدن")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="deals",
        verbose_name="مسئول معامله",
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "معامله"
        verbose_name_plural = "معاملات"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def is_closed(self):
        return self.stage.is_won or self.stage.is_lost