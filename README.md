# CRM با Django

پروژه اصلی (settings): `core`

## ساختار اپ‌ها
- **accounts** — کاربران، نقش‌ها (ادمین، مدیر فروش، کارشناس فروش، پشتیبانی) و پروفایل
- **contacts** — شرکت‌ها (Company)، سرنخ‌ها (Lead) و مخاطبین/مشتریان (Contact)
- **deals** — پایپ‌لاین فروش (Pipeline)، مراحل (Stage) و معاملات (Deal)
- **activities** — تسک (Task)، یادداشت (Note)، تماس (Call) و جلسه (Meeting) — همه با اتصال عمومی (GenericForeignKey) به Lead/Contact/Deal

## نصب و اجرا

```bash
python -m venv venv
source venv/bin/activate      # ویندوز: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations accounts contacts deals activities
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver
```

سپس:
- پنل ادمین: http://127.0.0.1:8000/admin/
- داشبورد معاملات: http://127.0.0.1:8000/
- تخته پایپ‌لاین: http://127.0.0.1:8000/pipeline/
- مخاطبین: http://127.0.0.1:8000/contacts/
- سرنخ‌ها: http://127.0.0.1:8000/contacts/leads/
- تسک‌های من: http://127.0.0.1:8000/activities/tasks/

## نکته مهم
اول از پنل ادمین یک `Pipeline` (مثلاً "فروش مستقیم") و چند `Stage` داخلش
(مثلاً: تماس اولیه، ارسال پیشنهاد، مذاکره، برد، باخت) بسازید تا بتوانید Deal ثبت کنید.

## مراحل بعدی پیشنهادی
- اضافه کردن اپ `communications` برای لاگ ایمیل/پیامک
- اضافه کردن اپ `invoices` برای فاکتور و پرداخت
- اضافه کردن اپ `reports` برای گزارش‌گیری و نمودار
- اضافه کردن REST API با Django REST Framework