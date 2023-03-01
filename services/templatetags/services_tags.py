from django import template

from services.models import ServicePage


register = template.Library()


@register.simple_tag
def services():
    return ServicePage.get_active_services()
