from django.conf import settings
from django.db import models


class Company(models.Model):
    """شرکت / سازمان مشتری"""

    name = models.CharField(max_length=200, verbose_name="نام شرکت")
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=100, blank=True, verbose_name="صنعت")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="companies",
        verbose_name="مسئول",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "شرکت"
        verbose_name_plural = "شرکت‌ها"
        ordering = ["name"]

    def __str__(self):
        return self.name


class LeadStatus(models.TextChoices):
    NEW = "new", "جدید"
    CONTACTED = "contacted", "در حال پیگیری"
    QUALIFIED = "qualified", "واجد شرایط"
    CONVERTED = "converted", "تبدیل‌شده به مشتری"
    LOST = "lost", "از دست رفته"


class LeadSource(models.TextChoices):
    WEBSITE = "website", "وب‌سایت"
    REFERRAL = "referral", "معرفی"
    ADVERTISEMENT = "ad", "تبلیغات"
    SOCIAL_MEDIA = "social", "شبکه‌های اجتماعی"
    COLD_CALL = "cold_call", "تماس سرد"
    OTHER = "other", "سایر"


class Lead(models.Model):
    """سرنخ فروش - قبل از تبدیل شدن به مشتری (Contact)"""

    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="نام خانوادگی")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    company_name = models.CharField(max_length=200, blank=True, verbose_name="نام شرکت")
    source = models.CharField(max_length=20, choices=LeadSource.choices, default=LeadSource.OTHER)
    status = models.CharField(max_length=20, choices=LeadStatus.choices, default=LeadStatus.NEW)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leads",
        verbose_name="مسئول پیگیری",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "سرنخ"
        verbose_name_plural = "سرنخ‌ها"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class Contact(models.Model):
    """مخاطب / مشتری تایید شده (بعد از تبدیل Lead یا ثبت مستقیم)"""

    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, blank=True, verbose_name="نام خانوادگی")
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    job_title = models.CharField(max_length=100, blank=True, verbose_name="سمت")
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
        verbose_name="شرکت",
    )
    converted_from_lead = models.OneToOneField(
        Lead,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="converted_contact",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
        verbose_name="مسئول",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "مخاطب"
        verbose_name_plural = "مخاطبین"
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()