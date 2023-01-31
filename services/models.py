from django.db import models
from wagtail.models import Page


class ServicePage(Page):
    beta_id = models.CharField("ID beta", max_length=255)
    beta_name = models.CharField("Nom du service", max_length=255)
    beta_pitch = models.CharField("Pitch", max_length=255)
    beta_link = models.URLField("Lien vers le service", max_length=255, blank=True)
    beta_problem = models.TextField("Le problème", blank=True)
    beta_service = models.TextField("Notre service", blank=True)
