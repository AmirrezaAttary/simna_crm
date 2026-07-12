from django import forms

from .models import Deal, Stage

INPUT = "w-full border border-gray-200 rounded-lg px-3.5 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-100 focus:border-indigo-400 transition"


class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = [
            "title", "pipeline", "stage", "contact", "company",
            "amount", "currency", "expected_close_date", "description",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": INPUT, "placeholder": "مثلاً قرارداد سالانه شرکت آریا"}),
            "pipeline": forms.Select(attrs={"class": INPUT, "id": "id_pipeline"}),
            "stage": forms.Select(attrs={"class": INPUT, "id": "id_stage"}),
            "contact": forms.Select(attrs={"class": INPUT}),
            "company": forms.Select(attrs={"class": INPUT}),
            "amount": forms.NumberInput(attrs={"class": INPUT}),
            "currency": forms.TextInput(attrs={"class": INPUT, "placeholder": "IRR"}),
            "expected_close_date": forms.DateInput(attrs={"class": INPUT, "type": "date"}),
            "description": forms.Textarea(attrs={"class": INPUT + " resize-none", "rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # اگه پایپ‌لاین قبلاً انتخاب شده (بعد از خطای فرم)، فقط مراحل همون پایپ‌لاین رو نشون بده
        pipeline_id = self.data.get("pipeline") or getattr(self.instance, "pipeline_id", None)
        if pipeline_id:
            self.fields["stage"].queryset = Stage.objects.filter(pipeline_id=pipeline_id)