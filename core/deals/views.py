from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from permissions.mixins import RowLevelPermissionMixin

from .models import Deal


class DealListView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Deal
    template_name = "deals/deal_list.html"
    context_object_name = "deals"
    paginate_by = 25
    feature_codename = "deals"
    owner_field = "owner"


class DealDetailView(LoginRequiredMixin, RowLevelPermissionMixin, DetailView):
    model = Deal
    template_name = "deals/deal_detail.html"
    context_object_name = "deal"
    feature_codename = "deals"
    owner_field = "owner"


class PipelineBoardView(LoginRequiredMixin, RowLevelPermissionMixin, ListView):
    model = Deal
    template_name = "deals/pipeline_board.html"
    context_object_name = "deals"
    feature_codename = "deals"
    owner_field = "owner"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .models import Pipeline, Stage

        pipeline = Pipeline.objects.prefetch_related("stages").first()
        if pipeline:
            context["pipeline"] = pipeline
            context["stages"] = pipeline.stages.all()

            # سازمان‌دهی معاملات بر اساس Stage
            deals_by_stage = {}
            for stage in context["stages"]:
                deals_by_stage[stage.id] = [
                    deal for deal in context["deals"] if deal.stage_id == stage.id
                ]
            context["deals_by_stage"] = deals_by_stage

        return context
