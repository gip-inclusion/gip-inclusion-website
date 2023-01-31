from django.views.generic.list import ListView

from services.models import ServicePage


class ServicesListView(ListView):
    model = ServicePage
