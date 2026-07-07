from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Deal, Pipeline


class DealListView(LoginRequiredMixin, ListView):
    model = Deal
    template_name = "deals/deal_list.html"
    context_object_name = "deals"
    paginate_by = 25


class DealDetailView(LoginRequiredMixin, DetailView):
    model = Deal
    template_name = "deals/deal_detail.html"
    context_object_name = "deal"


@login_required
def pipeline_board(request):
    """نمایش تخته کانبان مراحل معاملات (Kanban) برای پایپ‌لاین پیش‌فرض"""
    pipeline = Pipeline.objects.filter(is_default=True).first() or Pipeline.objects.first()
    stages = pipeline.stages.prefetch_related("deals").order_by("order") if pipeline else []
    return render(request, "deals/pipeline_board.html", {"pipeline": pipeline, "stages": stages})