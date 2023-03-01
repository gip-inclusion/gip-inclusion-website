from django.views.generic.list import ListView

from services.models import ServicePage


class ServicesListView(ListView):
    model = ServicePage

    def get_queryset(self):
        return ServicePage.get_active_services()

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["breadcrumb_data"] = {"current": "Nos services numériques"}
        return context
