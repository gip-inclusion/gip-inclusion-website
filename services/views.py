from django.views.generic.list import ListView

from services.enums import Phase
from services.models import ServicePage


class ServicesListView(ListView):
    model = ServicePage

    def get_queryset(self):
        return ServicePage.objects.exclude(beta_last_phase=Phase.ALUMNI)
