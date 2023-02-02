from django.views.generic.list import ListView

from services.enums import Phase
from services.form import FilterForm
from services.models import ServicePage


class ServicesListView(ListView):
    model = ServicePage

    def get_phase(self):
        filter_phase = self.request.GET.get("phase", None)
        return filter_phase if filter_phase in Phase.values else None

    def get_queryset(self):
        qs = ServicePage.objects.all()
        filter_phase = self.get_phase()
        if filter_phase:
            qs = qs.filter(beta_last_phase=filter_phase)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print(self.get_phase())
        context["form"] = FilterForm(initial={"phase": self.get_phase()})
        return context
